# autokey2espanso

Convert AutoKey phrase entries into Espanso YAML configuration.

## Why?

If you are migrating from AutoKey to Espanso, this tool converts your existing phrase entries automatically.

It reads matching `.json` and `.txt` pairs and generates a valid Espanso `matches:` configuration.

---

## Requirements

* Python 3.8+

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourname/autokey2espanso.git
cd autokey2espanso
pip install .
```

Or run directly:

```bash
python3 autokey2espanso/cli.py <directory>
```

---

## Usage

Basic usage (prints YAML to stdout):

```bash
autokey2espanso /path/to/autokey/phrases
```

Write output to file:

```bash
autokey2espanso /path/to/autokey/phrases -o espanso.yml
```

Verbose mode:

```bash
autokey2espanso /path/to/autokey/phrases -o espanso.yml -v
```

Word mode (`-w / --wordmode`):

```bash
autokey2espanso /path/to/autokey/phrases -o espanso.yml -w
```

Custom prefix (`-p / --prefix`):

```bash
autokey2espanso /path/to/autokey/phrases -p ":" -o espanso.yml
```

When enabled, the prefix will be added before each trigger.
If omitted, triggers are taken **1:1** from AutoKey.

When word mode is enabled, each entry will include:

```yaml
word: true
```

This is useful for triggers that should only match entire words in Espanso.

---

## How it works

For each entry, both files must exist:

```
Example.json
Example.txt
```

The first abbreviation inside the JSON file becomes the Espanso trigger. With optional prefix:

```json
"abbreviations": ["hello"]
```

Becomes with `-p ":"`:

```yaml
matches:
  - trigger: ":hello"
    replace: |
      Hello World!
```

Or 1:1 (no prefix):

```yaml
matches:
  - trigger: "hello"
    replace: |
      Hello World!
```

If word mode is enabled:

```yaml
matches:
  - trigger: ":hello"
    word: true
    replace: |
      Hello World!
```

---

## License

MIT
