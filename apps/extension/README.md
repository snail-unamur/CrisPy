# CrisPy — Python Static Analyzer

CrisPy is a rule-based static analysis extension that detects and explains
Python code issues directly in VS Code, with a focus on **performance**.

## Features

- **Real-time diagnostics** — issues are highlighted as you code
- **Performance-focused rules** — catch slow patterns early (NumPy, typing, mutability, and more)
- **Inline explanations** — every rule links to detailed documentation
- **Per-project configuration** — customize rule severity via a `.crispy` file at your project root
- **Autocomplete for config** — VS Code suggests all available rules in `.crispy` files

## Requirements

- Python 3.10 or higher must be installed and available on your `PATH`

## Configuration

Create a `.crispy` file at the root of your project to override rule severity:

```json
{
  "prefer-numpy-array": "warning",
  "avoid-mutable-default-args": "error",
  "prefer-explicit-typing": "off"
}
```

Available severity levels: `off` · `info` · `warning` · `danger`

## Rule Categories

| ID    | Title              | Category    |
| ----- | ------------------ | ----------- |
| PY001 | Prefer NumPy Array | Performance |
| ...   | ...                | ...         |

Full rule documentation is available at the [CrisPy docs site](https://snail-crispy.netlify.app/).

## Contributing

See the [contribution guidelines](https://github.com/snail-unamur/CrisPy#readme).
Issues and PRs are welcome on [GitHub](https://github.com/snail-unamur/CrisPy/issues).

## License

MIT © [Snail-Unamur](https://github.com/snail-unamur)
