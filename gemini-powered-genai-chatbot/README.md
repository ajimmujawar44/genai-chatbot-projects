# Gemini-Powered GenAI Chatbot

**Author:** Ajim Sikandar Mujawar

A browser-based generative AI chatbot built with a vanilla HTML/CSS/JavaScript frontend and a FastAPI backend. The backend uses Google's Gemini API and Google Search grounding for up-to-date answers. It also handles common India date/time questions directly using the Asia/Kolkata timezone.

## Features

- Chat interface with dark/light theme toggle
- FastAPI backend with a `/api/chat` endpoint
- Gemini response generation through the Google Gen AI SDK
- Google Search grounding configured for current information
- Markdown-to-HTML response formatting
- India date/time handling using `Asia/Kolkata`
- Health endpoint at `/`

## Tech stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI, Pydantic
- **AI:** Google Gemini (`google-genai`)
- **Additional:** Google Search grounding, Markdown, python-dotenv

## Project structure

```text
gemini-powered-genai-chatbot/
├── backend/
│   ├── .env                 # Local secrets; ignored by Git
│   ├── .env.example         # Safe environment template
│   ├── config.py
│   ├── gemini_service.py
│   ├── index.py
│   └── requirements.txt
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── .gitignore
├── LICENSE
├── README.md
└── vercel.json
```

## Setup and run locally

### 1. Configure the Gemini API key

Create a Gemini API key in Google AI Studio, then create `backend/.env` from the included template:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
MODEL_NAME=gemini-3.8-flash
```

From the `gemini-powered-genai-chatbot` project directory, copy the template using the command for your shell:

```powershell
# Windows PowerShell
Copy-Item backend/.env.example backend/.env
```

```bash
# macOS / Linux
cp backend/.env.example backend/.env
```

Then replace the placeholder value in `backend/.env` with your API key. The `.env` file is intentionally excluded from Git. Never commit or share your real API key.

### 2. Create a virtual environment

Run these commands from the project root:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
```

### 3. Start the backend

```bash
cd backend
uvicorn index:app --reload
```

The API runs at http://127.0.0.1:8000. API documentation is available at http://127.0.0.1:8000/docs.

### 4. Open the frontend

With the backend running, open `frontend/index.html` in your browser.

> **Local API URL:** The current frontend is configured to call `http://127.0.0.1:8000/api/chat`. For deployment, update `API_URL` in `frontend/app.js` to your deployed backend URL or configure a same-origin relative API path.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Backend health response |
| `POST` | `/api/chat` | Generates an AI response |
| `GET` | `/api/current-time` | Returns current India date and time |

Example request:

```json
{
  "message": "Explain generative AI in simple words"
}
```

## Important production notes

- Replace the permissive CORS configuration in `backend/index.py` with your actual frontend origin before production.
- Store `GEMINI_API_KEY` in your deployment provider's environment-variable settings; do not upload `.env`.
- The current frontend uses a fixed local API URL. Configure it for your deployment before publishing.
- Review and pin dependency versions before a production release.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
