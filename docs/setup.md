# Getting Started

Run Phil locally — no Docker required.

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | `python3 --version` |
| Node.js | 20+ | `node --version` |
| Anthropic API key | — | [console.anthropic.com](https://console.anthropic.com) |
| Google Workspace account | — | Gmail + Google Calendar access |

!!! note "DE — Voraussetzungen"
    Python 3.11+, Node 20+, ein Anthropic API-Key und ein Google Workspace Konto.
    Die `.env.example` erklärt jeden Parameter.

---

## Step 1: Clone and install

```bash
git clone https://github.com/swrobuts/phil-knowledge-navigator.git
cd phil-knowledge-navigator

# Python dependencies
pip install -r backend/requirements.txt

# JavaScript dependencies
cd frontend
npm install
cd ..
```

---

## Step 2: Configure `.env`

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in:

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | Your Claude API key |
| `OPENAI_API_KEY` | Optional | For OpenAI embeddings (ChromaDB) |
| `GOG_ACCOUNT` | For mail/calendar | Your Google Workspace email |
| `GOG_KEYRING_PASSWORD` | For mail/calendar | App password or OAuth token |
| `LOCAL_LLM_ENDPOINT` | Optional | LM Studio local LLM endpoint |
| `LOCAL_LLM_MODEL` | Optional | e.g. `qwen2.5-32b-instruct` |

!!! warning
    Never commit your `.env` file. It is listed in `.gitignore`.
    The repo only contains `.env.example` with placeholder values.

---

## Step 3: Google Workspace authentication

Phil connects to Gmail and Google Calendar via the Exchange Web Services (EWS) protocol.

1. Enable "Less Secure Apps" or generate an **App Password** in your Google Account
2. Set `GOG_ACCOUNT` to your full Google email address
3. Set `GOG_KEYRING_PASSWORD` to the generated App Password

!!! note "DE"
    Phil nutzt EWS (Exchange Web Services) für den Zugriff auf Gmail und Google Calendar.
    Du brauchst ein App-Passwort, das du in den Google-Kontoeinstellungen unter
    "Sicherheit → App-Passwörter" erstellen kannst.

---

## Step 4: Run Phil

```bash
# Terminal 1 — Backend (FastAPI)
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend (Vite dev server)
cd frontend
npm run dev
```

Open your browser at **[http://localhost:5173](http://localhost:5173)**

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'backend'`**
Run `uvicorn` from the repo root, not from inside `backend/`.

**`ChromaDB SIGBUS error`**
ChromaDB uses memory-mapped files that must not live on OneDrive or network drives.
Phil stores them at `/tmp/phil_chroma` automatically.

**Mail/calendar returns empty**
Check your `.env` credentials. Run `GET /api/mails` directly to see the raw response.

**LLM returns errors**
Verify your `ANTHROPIC_API_KEY` is valid and has remaining credits.
Phil will fall back to cloud automatically if a local LLM is configured but unavailable.
