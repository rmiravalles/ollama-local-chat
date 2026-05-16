import os

from flask import Flask, render_template, request, session
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable '{name}'. Add it to your .env file."
        )
    return value


OLLAMA_BASE_URL = get_required_env("OLLAMA_BASE_URL")
OLLAMA_MODEL_NAME = get_required_env("OLLAMA_MODEL_NAME")
OLLAMA_API_KEY = get_required_env("OLLAMA_API_KEY")

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OLLAMA_API_KEY,
)


def validate_ollama_configuration() -> None:
    models = client.models.list()
    available_models = {model.id for model in models.data}

    if OLLAMA_MODEL_NAME not in available_models:
        raise RuntimeError(
            f"Model '{OLLAMA_MODEL_NAME}' is not available from Ollama at {OLLAMA_BASE_URL}."
        )


def get_chat_history() -> list[dict[str, str]]:
    history = session.get("chat_history", [])
    if not isinstance(history, list):
        return []
    return [message for message in history if isinstance(message, dict)]


def set_chat_history(history: list[dict[str, str]]) -> None:
    session["chat_history"] = history

@app.route("/", methods=["GET", "POST"])
def index():
    error_text = ""
    user_message = ""
    chat_history = get_chat_history()

    if request.method == "POST" and request.form.get("action") == "clear":
        session.pop("chat_history", None)
        chat_history = []
        return render_template(
            "index.html",
            error="",
            prompt="",
            model_name=OLLAMA_MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
            chat_history=chat_history,
        )

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()

        if not user_message:
            error_text = "Please enter a message before sending."
        else:
            try:
                chat_history = chat_history + [{"role": "user", "content": user_message}]
                response = client.chat.completions.create(
                    model=OLLAMA_MODEL_NAME,
                    messages=chat_history,
                )
                response_text = response.choices[0].message.content or ""
                chat_history = chat_history + [
                    {"role": "assistant", "content": response_text}
                ]
                set_chat_history(chat_history)
            except Exception:
                app.logger.exception("Failed to generate an Ollama response")
                error_text = (
                    "Could not reach Ollama or generate a response. "
                    "Check that Ollama is running and the selected model is available."
                )

    return render_template(
        "index.html",
        error=error_text,
        prompt=user_message,
        model_name=OLLAMA_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        chat_history=chat_history,
    )

if __name__ == "__main__":
    validate_ollama_configuration()
    app.run(debug=True)