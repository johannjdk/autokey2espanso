#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def verbose_print(enabled, message):
    if enabled:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}", file=sys.stderr)


def collect_entries(directory: Path, verbose: bool, prefix: str):
    entries = []
    json_files = sorted(directory.glob("*.json"))

    verbose_print(verbose, f"Scanning directory: {directory}")
    verbose_print(verbose, f"Found {len(json_files)} JSON files")

    for json_file in json_files:
        base_name = json_file.stem
        txt_file = directory / f"{base_name}.txt"

        if not txt_file.exists():
            verbose_print(verbose, f"Skipping '{base_name}': missing .txt file")
            continue

        try:
            with json_file.open("r", encoding="utf-8") as jf:
                data = json.load(jf)
        except Exception as e:
            verbose_print(verbose, f"Skipping '{base_name}': JSON error ({e})")
            continue

        abbreviations = (
            data.get("abbreviation", {})
            .get("abbreviations", [])
        )

        if not abbreviations:
            verbose_print(verbose, f"Skipping '{base_name}': no abbreviation found")
            continue

        trigger = abbreviations[0]
        if prefix:
            trigger = f"{prefix}{trigger}"

        try:
            with txt_file.open("r", encoding="utf-8") as tf:
                content = tf.read().rstrip()
        except Exception as e:
            verbose_print(verbose, f"Skipping '{base_name}': TXT read error ({e})")
            continue

        entries.append((trigger, content))
        verbose_print(verbose, f"Processed '{base_name}' -> trigger '{trigger}'")

    verbose_print(verbose, f"Successfully processed {len(entries)} entries")
    return entries


def generate_yaml(entries, wordmode=False):
    lines = ["matches:"]
    for trigger, content in entries:
        lines.append(f"  - trigger: \"{trigger}\"")
        if wordmode:
            lines.append("    word: true")
        lines.append("    replace: |-")
        for line in content.splitlines():
            lines.append(f"      {line}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Convert AutoKey phrase entries to Espanso YAML format."
    )
    parser.add_argument("directory", help="Directory containing AutoKey entries")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument(
        "-w", "--wordmode", action="store_true", help="Add 'word: true' to each entry"
    )
    parser.add_argument(
        "-p", "--prefix", help="Custom prefix to add to triggers", default=""
    )
    args = parser.parse_args()

    directory = Path(args.directory)

    if not directory.is_dir():
        print("Error: Invalid directory", file=sys.stderr)
        sys.exit(1)

    entries = collect_entries(directory, args.verbose, args.prefix)
    yaml_output = generate_yaml(entries, wordmode=args.wordmode)

    if args.output:
        output_path = Path(args.output)
        try:
            with output_path.open("w", encoding="utf-8") as f:
                f.write(yaml_output)
            verbose_print(args.verbose, f"YAML written to {output_path}")
            sys.exit(0)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(yaml_output, end="")
        sys.exit(0)


if __name__ == "__main__":
    main()
