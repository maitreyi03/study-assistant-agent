"""Project configuration and environment-variable loading."""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parent.parent
NOTES_FILE = PROJECT_DIR / "study_notes.json"
ENV_FILE = PROJECT_DIR / ".env"

MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_TEMPERATURE = 0.2
THREAD_ID = "student-session-1"


def load_environment() -> None:
    """Load the local environment and verify required settings."""
    load_dotenv(ENV_FILE)

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "\nMissing GROQ_API_KEY.\n\n"
            "1. Copy .env.example to a new file named .env\n"
            "2. Open .env and replace the placeholder with your Groq API key\n"
            "3. Run the application again\n"
        )
