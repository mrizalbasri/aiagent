# AI Agent (Python)

A small AI coding agent built with Python, the OpenAI SDK, and OpenRouter. It can inspect a project, read files, run Python programs, and write or modify files by calling tools through an LLM-driven feedback loop.

This project was built as part of the [Boot.dev](https://www.boot.dev) course **Build an AI Agent in Python**.

## Features

- **Function calling / tool use** — the LLM selects from four tools:
  - `get_files_info` — list files and directories
  - `get_file_content` — read a file's contents
  - `run_python_file` — execute a Python file with optional arguments
  - `write_file` — create or overwrite a file
- **Agent loop** — the model iterates (up to 20 turns), using tool results to plan its next step until it produces a final answer.
- **Conversation history** — every assistant tool call and matching `tool` result is appended to the message history.
- **Workspace sandboxing** — all file operations are confined to `./calculator`; paths outside it are rejected.
- **Sample project** — a small CLI calculator in `calculator/` used to demo the agent (including fixing a real bug).

## Project Structure

```
.
├── main.py                  # CLI entry point + agent loop
├── call_function.py         # Tool registry and tool-call dispatcher
├── prompts.py               # System prompt
├── config.py                # Shared config (max file read size)
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py        # Each module exports a function + its JSON schema
├── calculator/              # Sandbox workspace the agent operates on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
├── test_*.py                # Unit tests for the individual tools
└── pyproject.toml
```

## Requirements

- Python **3.14+**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- An [OpenRouter](https://openrouter.ai/) API key

## Setup

1. Clone the repository and install dependencies:

   ```sh
   uv sync
   ```

2. Create your environment file:

   ```sh
   cp .env.example .env
   ```

3. Add your OpenRouter API key to `.env`:

   ```dotenv
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

## Usage

Ask the agent to do something:

```sh
uv run main.py "what files are in the working directory?"
uv run main.py "read the contents of main.py"
uv run main.py "run tests.py"
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
```

Add `--verbose` to see the tool arguments and each function's output:

```sh
uv run main.py "how does the calculator render results to the console?" --verbose
```

The agent prints each tool it calls (for example `- Calling function: get_files_info`) and finishes with a `Final response:` section.

## How It Works

1. The system prompt tells the model which operations are available and that paths are relative to the working directory.
2. The tool schemas in `call_function.py` are passed to `chat.completions.create` as `tools`.
3. When the model returns `tool_calls`, `call_function()` parses the JSON arguments, injects the sandboxed `working_directory`, runs the matching Python function, and returns a `role: "tool"` message.
4. That result is appended to the conversation and the loop calls the model again.
5. When the model returns plain text instead of tool calls, the loop ends and prints the final response.

## Manual Tool Checks

The root `test_*.py` files are small demo scripts that exercise each tool directly against the `calculator/` workspace and print the results:

```sh
uv run python test_get_files_info.py
uv run python test_get_file_content.py
uv run python test_run_python_file.py
uv run python test_write_file.py
```

Note: `test_write_file.py` writes to files under `calculator/`, so run it only after committing any work you care about.

## Security Notes

This is a learning project, **not** a production-ready agent.

- The agent can write files and execute Python code inside `./calculator`. Never point it at a directory containing data you cannot afford to lose.
- API keys live in `.env`, which is git-ignored. Never commit real credentials — use `.env.example` as the template.
- Set a credit limit on your OpenRouter key to avoid unexpected charges.
- Commit or back up your work before letting the agent modify a codebase.

## License

This project is provided for educational purposes. See the Boot.dev course for the original assignment.
