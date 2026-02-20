# autokey2espanso

Convert AutoKey phrase entries into Espanso YAML configuration.

## Why?

If you are migrating from AutoKey to Espanso, this tool converts your existing phrase entries automatically.

It reads matching `.json` and `.txt` pairs and generates a valid Espanso `matches:` configuration.

---

## Requirements

- Python 3.8+

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourname/autokey2espanso.git
cd autokey2espanso
pip install .
````

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

---

## How it works

For each entry, both files must exist:

```
Example.json
Example.txt
```

The first abbreviation inside the JSON file becomes the Espanso trigger:

```json
"abbreviations": ["hello"]
```

Becomes:

```yaml
matches:
  - trigger: ":hello"
    replace: |
      Hello World!
```

---

## License

MIT
# autokey2espanso
