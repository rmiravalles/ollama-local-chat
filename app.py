import os

from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)


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

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    error_text = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()

        if not user_message:
            error_text = "Please enter a message before sending."
        else:
            try:
                response = client.chat.completions.create(
                    model=OLLAMA_MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": user_message,
                        }
                    ],
                )
                response_text = response.choices[0].message.content or ""
            except Exception:
                app.logger.exception("Failed to generate an Ollama response")
                error_text = (
                    "Could not reach Ollama or generate a response. "
                    "Check that Ollama is running and the selected model is available."
                )

    return render_template(
        "index.html",
        response=response_text,
        error=error_text,
        prompt=user_message,
        model_name=OLLAMA_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
    )

if __name__ == "__main__":
    validate_ollama_configuration()
    app.run(debug=True)