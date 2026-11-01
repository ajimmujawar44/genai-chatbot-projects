# Simple FastAPI Chatbot Starter

**Author:** Ajim Sikandar Mujawar

A minimal FastAPI starter project from the supplied archive. The current implementation exposes a single `/` endpoint that returns a JSON message. It is a backend/API starter and **does not yet include an AI model, chat endpoint, or chatbot frontend**.

## Project structure

```text
simple-fastapi-chatbot-starter/
├── app/
│   └── main.py
├── .env
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── vercel.json
```

## Features

- Minimal FastAPI application
- JSON response from the root endpoint
- Ready for extension with a chat route and an LLM provider

## Run locally

Python 3.10+ is recommended.

```bash
# Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

Open:
- API: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs

## Environment variables

Copy `.env.example` to `.env` and adjust values if needed. The current starter endpoint does not require environment variables.

## Next improvements

- Add a `POST /api/chat` endpoint
- Connect an LLM provider (for example, Gemini or OpenAI)
- Add request validation, error handling, and a frontend
- Restrict CORS origins before production deployment

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
