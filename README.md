# Ollama local chat

Local web chat application that connects to an Ollama model through a Flask server.

The project is designed to provide a simple local-first chat interface where prompts are submitted from a browser, forwarded to Ollama, and the model response is rendered back in the page.

## Purpose

- Run a local LLM through Ollama using a lightweight Python backend.
- Expose a minimal browser UI for prompt/response interaction.
- Keep model endpoint and model selection configurable through `.env`.

## Tools and Technologies

- Python: runtime language for the backend.
- Flask: web framework used to serve the UI and handle form submissions.
- OpenAI Python SDK: client used against Ollama's OpenAI-compatible API.
- python-dotenv: loads environment variables from `.env`.
- Ollama: local model runtime.
- HTML/Jinja template: simple server-rendered interface.

## Project Structure

- `app.py`: Flask application, environment loading, Ollama client configuration, and request handling.
- `templates/index.html`: chat UI template.
- `.env`: local configuration values.
- `requirements.txt`: Python dependencies.

## Prerequisites

- Python 3.10+ (3.11+ recommended).
- Ollama installed and running locally.
- A pulled Ollama model (for example `qwen2.5:1.5b`).

## Setup

1. Clone the repository and move into the project directory.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Ensure Ollama is running.
5. Pull the model you want to use.

Example commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama serve
# in another terminal
ollama pull qwen2.5:1.5b
```

## Configuration with `.env`

The app requires the following variables in `.env`:

```env
OLLAMA_BASE_URL="http://localhost:11434/v1"
OLLAMA_MODEL_NAME="qwen2.5:1.5b"
OLLAMA_API_KEY="ollama"
```

Notes:

- `OLLAMA_BASE_URL` must point to Ollama's OpenAI-compatible endpoint.
- `OLLAMA_MODEL_NAME` must match a model available in your local Ollama instance.
- `OLLAMA_API_KEY` is required by the SDK interface; for local Ollama this is commonly `ollama`.

If any required variable is missing, the app raises a startup error with a clear message.

## How to Run

From the project directory (with the virtual environment active):

```bash
python app.py
```

Then open:

- `http://127.0.0.1:5000`

On startup, the app validates that:

- Ollama is reachable.
- The configured model exists.

If validation fails, the app exits early and prints the reason.

## How to Use

1. Open the web page.
2. Enter a prompt in the textarea.
3. Click `Send`.
4. Read the model response shown under `Response`.

Current behavior:

- Empty prompts are rejected with an inline error message.
- Prompt text is preserved after submission.
- Errors contacting Ollama are shown in the UI and logged by Flask.

## Troubleshooting

- App says a required environment variable is missing:
	Confirm `.env` exists and includes all required keys.
- Model not available error at startup:
	Run `ollama list` and update `OLLAMA_MODEL_NAME` or pull the missing model.
- Could not reach Ollama:
	Ensure `ollama serve` is running and `OLLAMA_BASE_URL` is correct.
- Import errors:
	Reinstall dependencies with `pip install -r requirements.txt`.

## Future Improvements

- Multi-turn conversation history.
- Streaming token output.
- Markdown/code rendering in responses.
- Automated tests for route behavior and startup validation.