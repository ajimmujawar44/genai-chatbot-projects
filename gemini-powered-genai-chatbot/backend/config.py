import os
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.8-flash")

    @staticmethod
    def validate():
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                f"Missing GEMINI_API_KEY! Check your .env file at: {ENV_FILE}"
            )