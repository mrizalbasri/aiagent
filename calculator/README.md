# Calculator

A tiny CLI calculator used as the sandbox workspace for the AI agent.

## Usage

From the repository root:

```sh
uv run calculator/main.py "3 + 5"
uv run calculator/main.py "3 + 7 * 2"
```

It prints the expression and result as formatted JSON:

```json
{
  "expression": "3 + 7 * 2",
  "result": 17
}
```

## Tests

From the repository root:

```sh
uv run calculator/tests.py
```

The calculator lives in `pkg/calculator.py` (expression evaluation) and `pkg/render.py` (JSON output formatting).
