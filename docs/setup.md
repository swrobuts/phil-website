# Getting Started

Three ways to run Phil — pick the one that fits:

| Method | Prerequisites | Time | Best for |
|--------|--------------|------|---------|
| **Docker Hub** | Docker only | ~2 min | Quickest start, no dev tools needed |
| **Docker Compose (build)** | Docker + Git | ~5 min | Local testing with source code |
| **Dev mode** | Python 3.12, Node 20, Git | ~20 min | Development and customisation |

---

## Option A — Docker Hub (fastest)

No Python, no Node, no Git required. Just Docker and a `.env` file.

**Step 1 — Install Docker**

Download [Docker Desktop](https://www.docker.com/get-docker) (free, works on Mac, Windows, Linux). Start it and confirm `docker info` runs without errors.

**Step 2 — Create your `.env` file**

Download the example and fill it in:

```bash
curl -o backend.env https://raw.githubusercontent.com/swrobuts/phil-knowledge-navigator/main/backend/.env.example
# Edit backend.env — fill in at minimum:
#   ANTHROPIC_API_KEY=sk-ant-...
#   GOG_ACCOUNT=you@gmail.com
```

**Step 3 — Run**

```bash
docker run -d \
  --name phil \
  -p 8000:8000 \
  --env-file backend.env \
  swrobutsdocker/phil:latest
```

Open **[http://localhost:8000](http://localhost:8000)**. That's it.

**Managing the container:**

```bash
# Stop
docker stop phil && docker rm phil

# Update to latest version
docker pull swrobutsdocker/phil:latest
docker stop phil && docker rm phil
docker run -d --name phil -p 8000:8000 --env-file backend.env swrobutsdocker/phil:latest

# View logs
docker logs -f phil
```

!!! tip "Image on Docker Hub"
    `swrobutsdocker/phil` is a public image — no Docker Hub account needed to pull it.

---

## Option B — Docker Compose (build from source)

Use this if you want to run the source code locally without setting up Python and Node manually.

**Prerequisites:** [Docker Desktop](https://www.docker.com/get-docker) + Git

```bash
git clone https://github.com/swrobuts/phil-knowledge-navigator.git
cd phil-knowledge-navigator

cp backend/.env.example backend/.env
# (edit backend/.env)

docker compose -f docker-compose.local.yml up --build
```

Open **[http://localhost:8000](http://localhost:8000)**.

---

## Option C — Dev mode (full setup)

Use this for active development. Hot-reload for both frontend and backend.

**Time to first run: ~20 minutes** (faster if Python and Node are already installed)

### What you will need

| Requirement | Minimum version | How to check |
|-------------|----------------|-------------|
| Python | 3.12 | `python3 --version` |
| Node.js | 20 | `node --version` |
| npm | 9 | `npm --version` |
| Git | any | `git --version` |
| A text editor | — | VS Code recommended |

Don't have these yet? See the [install helpers](#install-helpers) at the bottom of this page.

---

## Step 1 — Clone the repository

```bash
git clone https://github.com/swrobuts/phil-knowledge-navigator.git
cd phil-knowledge-navigator
```

If you don't have Git: download the ZIP from the GitHub repository page (green "Code" button → "Download ZIP"), unzip it, and open a terminal in that folder.

---

## Step 2 — Create a Python virtual environment

Always use a virtual environment. This isolates Phil's dependencies from the rest of your system and prevents version conflicts.

```bash
python3 -m venv .venv
```

Then **activate** it. The command depends on your operating system:

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows (Command Prompt)"

    ```cmd
    .venv\Scripts\activate.bat
    ```

=== "Windows (PowerShell)"

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

Your terminal prompt should now start with `(.venv)`. You'll need to do this every time you open a new terminal.

---

## Step 3 — Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

This installs FastAPI, exchangelib, RDFlib, ChromaDB, and all other backend libraries. Expect it to take 1–3 minutes.

If you see `pip: command not found`, try `pip3` instead.

---

## Step 4 — Install JavaScript dependencies

```bash
cd frontend
npm install
cd ..
```

This installs React, Vite, TypeScript, and all frontend dependencies. They go into `frontend/node_modules/` and are not uploaded to GitHub.

---

## Step 5 — Configure your environment file

Copy the example file and open it in your text editor:

```bash
cp backend/.env.example backend/.env
```

Now open `backend/.env`. Here is every variable explained:

### AI / LLM settings

| Variable | Required | What to put here |
|----------|----------|-----------------|
| `ANTHROPIC_API_KEY` | ✅ for cloud LLM | Your Claude API key (starts with `sk-ant-`) |
| `OPENAI_API_KEY` | ✅ for TTS + search | OpenAI key for embeddings and text-to-speech (starts with `sk-proj-`) |
| `LOCAL_LLM_ENDPOINT` | Optional | `http://localhost:1234/v1` (LM Studio default) |
| `LOCAL_LLM_MODEL` | Optional | e.g. `qwen2.5-32b-instruct` |

**LLM:** You need at least one of `ANTHROPIC_API_KEY` or `LOCAL_LLM_ENDPOINT`. If both are set, Phil tries the local endpoint first and falls back to Anthropic.

**OpenAI:** Used for ChromaDB embeddings (semantic search over your emails) and the text-to-speech "read aloud" feature. These features are silently disabled if the key is missing.

### Google Calendar settings

| Variable | Required | What to put here |
|----------|----------|-----------------|
| `GOG_ACCOUNT` | For Google Calendar | Your Gmail address (e.g. `you@gmail.com`) |
| `GOG_KEYRING_PASSWORD` | In Docker only | Keyring password for the gog OAuth token |

Exchange / IMAP credentials are entered via the **login screen**, not in `.env`.
See [Step 6](#step-6--connect-your-email-and-calendar) for full instructions.

!!! warning "Never commit your .env file"
    The `.env` file contains your secrets. It is listed in `.gitignore` — Git will not track it. If you accidentally commit it, rotate your API keys immediately.

---

## Step 6 — Connect your email and calendar

Phil has two separate mail/calendar backends that work independently:

- **Exchange / IMAP** — for reading email and syncing tasks (credentials entered via login UI)
- **Google Calendar** — for calendar events (requires the `gog` CLI binary + OAuth)

### 6a — Exchange / IMAP login

Phil's login screen supports four institutions out of the box. The credentials you enter there are **never written to disk** — they are held in the server's memory only for the duration of your session.

=== "THWS (Würzburg-Schweinfurt)"

    - Protocol: IMAP (port 993 SSL) for email + EWS for calendar and tasks
    - Server: `webmail.thws.de`
    - Username: your short login name (e.g. `mmueller`) **or** full email (`max.mueller@fhws.de`)
    - Password: your THWS/RZ password

    Phil tries both `mmueller` and `mmueller@fhws.de` automatically if you enter the short form.

    Official THWS mail client setup guide: [itsc.thws.de → THWS-Mail einrichten](https://itsc.thws.de/itsc/hochschulweite-dienste/thws-mail/einrichtung-e-mail-client/)

=== "Microsoft 365 / generic Exchange"

    - Protocol: EWS
    - Username: full email address
    - Password: your Microsoft 365 / domain password
    - EWS URL: Phil uses autodiscover by default; THWS is the only hardcoded exception

=== "No email account (demo mode)"

    You can run Phil without any mail connection. The mail and tasks views will be empty, but chat, calendar (if `gog` is configured), the knowledge graph, and the LLM all work normally.

    Simply click **Skip / Demo** on the login screen.

### 6b — Google Calendar (`gog` CLI)

Phil reads and writes Google Calendar events via the [`gog`](https://github.com/nicholasgasior/gog) CLI binary. This is a separate OAuth-based tool that stores your Google tokens in the system keyring.

**Install gog:**

=== "macOS (Homebrew)"

    ```bash
    brew install nicholasgasior/tap/gog
    ```

=== "Linux / manual install"

    Download the latest binary from the [gog GitHub releases page](https://github.com/nicholasgasior/gog/releases) and place it in `~/bin/gog` or anywhere in your `$PATH`:

    ```bash
    chmod +x ~/bin/gog
    ```

=== "Verify"

    ```bash
    gog version
    gog --help
    ```

**Authenticate gog:**

```bash
gog auth login
```

This opens a browser window for Google OAuth. After authorising, gog stores the token in your system keyring.

**Configure Phil:**

```bash
# In backend/.env:
GOG_ACCOUNT=your.name@gmail.com
```

**Verify calendar access:**

```bash
gog calendar events --account your.name@gmail.com --max 5
```

You should see your next 5 events as JSON.

!!! warning "Docker and the keyring"
    Inside a Docker container there is no GUI keyring. To use Google Calendar in Docker, you need to export the OAuth token password:

    1. On the host (after `gog auth login`): the token is stored in your system keyring. The `GOG_KEYRING_PASSWORD` is the password that protects the keyring file.
    2. Set `GOG_KEYRING_PASSWORD=your-keyring-password` in `backend/.env` before running Docker.
    3. Phil passes this variable to `gog` so it can unlock the keyring without a GUI.

---

## Step 7 — Get an LLM

Phil supports local and cloud LLMs. **Local is the recommended default** for two reasons:

- **Cost:** Running a local model is free after the hardware investment. Cloud APIs charge per token — the costs are low, but they accumulate over time.
- **DSGVO / data privacy:** With a local model, your emails, prompts, and personal data never leave your machine. Cloud APIs transmit your data to external servers (US jurisdiction), which is legally problematic for professional email in a German university or business context (Art. 25 DSGVO — privacy by design).

The Anthropic Claude API is supported as a **technical reference and quality baseline** — useful for benchmarking and demonstrations, but not the intended production setup.

!!! tip "Recommended: Local LM Studio"
    Set up LM Studio (free, offline, DSGVO-compliant) — no API costs, your data stays on your machine.

=== "Local — LM Studio ✓ Empfohlen"

    **System requirements:**

    | Model tier | Unified memory / VRAM | Quality |
    |-----------|----------------------|---------|
    | 7B Q4_K_M | 6 GB | Good for simple triage |
    | 14B Q4_K_M | 10 GB | Good balance |
    | 32B Q4_K_M | 22 GB | Best results, recommended |

    **Setup:**

    1. Download [LM Studio](https://lmstudio.ai) (free, works on Mac/Windows/Linux)
    2. In LM Studio: **Discover** tab → search for `Qwen2.5-32B-Instruct-Q4_K_M` (or a smaller model if your machine requires it)
    3. Download the model (10–30 min depending on size and connection)
    4. In LM Studio: **Local Server** tab → **Start Server** (listens on port 1234 by default)
    5. In `backend/.env`:
       ```
       LOCAL_LLM_ENDPOINT=http://localhost:1234/v1
       LOCAL_LLM_MODEL=qwen2.5-32b-instruct
       ```

    No email content, no prompts, no personal data ever leave your machine.

=== "Cloud — Anthropic Claude (Referenz / Demo)"

    !!! warning "Datenschutz-Hinweis"
        Mit einem Cloud-API-Key werden Ihre E-Mails und Prompts an externe Server (Anthropic, USA) übertragen. Für professionelle oder personenbezogene Daten empfehlen wir ausschließlich den Local-Modus.

    The Anthropic API is useful as a quality baseline and for demonstrations where local hardware is unavailable.

    1. Create a free account at [console.anthropic.com](https://console.anthropic.com)
    2. Go to **API Keys** → **Create Key**
    3. Copy the key into `backend/.env`:
       ```
       ANTHROPIC_API_KEY=sk-ant-api03-...
       ```

    **Cost:** Roughly €0.02–0.10 per session for typical daily use. You can set a monthly spending limit in the Anthropic console.

=== "Cloud — OpenAI-compatible APIs"

    Any OpenAI-compatible API endpoint (OpenAI, Mistral, Together AI, etc.) works via the local client interface:

    ```
    LOCAL_LLM_ENDPOINT=https://api.openai.com/v1
    LOCAL_LLM_ENDPOINT_KEY=sk-...your-key...
    LOCAL_LLM_MODEL=gpt-4o-mini
    ```

    The same data-privacy considerations as above apply — data leaves your machine.

---

## Step 8 — Run Phil

Open **two terminals**, both in the repo root, both with the virtual environment activated.

**Terminal 1 — Backend:**

```bash
uvicorn backend.main:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process ...
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in 400 ms
  ➜  Local:   http://localhost:5173/
```

Open **[http://localhost:5173](http://localhost:5173)** in your browser.

The login screen will ask for your Exchange/IMAP account (THWS, Microsoft 365, or generic IMAP). These credentials are held in memory for the session only — they are never written to disk.

!!! tip "Vite proxies /api automatically"
    The frontend dev server (port 5173) proxies all `/api/*` requests to the backend (port 8001). You never need to open port 8001 directly during development.

---

## Docker Compose (alternative to Steps 2–8)

If you have Docker installed, you can skip the Python/Node setup entirely.

**Install Docker:** [docker.com/get-docker](https://www.docker.com/get-docker) — Docker Desktop works on Mac, Windows, and Linux. It's free for personal use.

```bash
# 1. Clone the repo (same as Step 1)
git clone https://github.com/swrobuts/phil-knowledge-navigator.git
cd phil-knowledge-navigator

# 2. Create and fill in your .env (same as Steps 5–6)
cp backend/.env.example backend/.env
# (edit backend/.env with your credentials)

# 3. Start everything
docker compose up --build
```

Open **[http://localhost:8000](http://localhost:8000)**.

**What Docker builds:**

| Container | Port | What it does |
|-----------|------|-------------|
| `kn-mail` | 8000 | FastAPI serving both the API **and** the pre-built React frontend as static files |

Unlike the dev mode, Docker uses a single container. The Dockerfile uses a two-stage build: Node 20 compiles the React frontend, then the Python 3.12-slim image serves everything through uvicorn on port 8000.

To stop: `Ctrl+C`, then `docker compose -f docker-compose.local.yml down`.

To rebuild after code changes: `docker compose -f docker-compose.local.yml up --build`.

!!! tip "DSGVO / Data privacy"
    In local mode (with or without Docker), no emails, prompts, or personal data leave your machine. This applies as long as `LOCAL_LLM_ENDPOINT` is set to a local LM Studio instance and `ANTHROPIC_API_KEY` is not used. This design supports GDPR compliance under Art. 25 (privacy by design).

---

## Running the tests

Phil includes a test suite for the backend. Run it from the repo root:

```bash
pytest backend/tests/ -v
```

For a single test file:

```bash
pytest backend/tests/test_llm_client.py -v
```

If you see `pytest: command not found`, install it first: `pip install pytest`.

Expected output when everything is working:

```
PASSED backend/tests/test_mail_triage.py::test_categorise_vip_mail
PASSED backend/tests/test_llm_client.py::test_local_fallback
...
N passed in X.Xs
```

---

## Security considerations

!!! danger "Before sharing or deploying Phil"

    Phil is designed as a **local personal tool**, not a production service. Before running it for other people or exposing it to the internet, be aware of:

**API key exposure**

- Your `.env` file contains API keys and passwords. Never commit it. Never paste it into chat tools.
- If you suspect a key has been leaked: rotate it immediately in the Anthropic or Google console.

**Email data stays local**

- Phil stores email summaries and embeddings in ChromaDB (at `/tmp/phil_chroma` by default). This folder contains your mail data. Back it up, and delete it when you stop using Phil.

**No authentication hardening for public exposure**

- The default setup has a simple session-based login. It is **not hardened** for exposure to the internet.
- If you want to run Phil on a server, add a reverse proxy (nginx, Caddy) with HTTPS and access restriction.

**LLM prompt injection**

- Phil passes email content directly to the LLM. A malicious email could attempt prompt injection (trying to make Phil execute unintended commands). Phil does not currently have prompt injection defences. Do not use Phil to triage emails from untrusted sources in security-critical contexts.

**Local LLM vs cloud trade-off**

- Cloud LLMs (Anthropic Claude) transmit your email content to Anthropic's servers. For sensitive data (medical, legal, HR), use the local LLM mode exclusively.
- Anthropic's data retention policy: [anthropic.com/privacy](https://www.anthropic.com/privacy). By default, API inputs are not used for training.

---

## Known limitations and open risks

| Area | Current state | Risk |
|------|--------------|------|
| Mail sync | Pulls only the most recent N emails | Older emails are not indexed |
| Calendar | Google Calendar only in demo; Exchange required for full functionality | Some users need manual calendar entry |
| LLM hallucination | RAG reduces but does not eliminate hallucinations | Always verify AI-generated summaries against source emails |
| Knowledge graph | Built from email content only; no external data sources | Graph may miss entities not mentioned in recent emails |
| Session security | Local single-user setup; no multi-user isolation | Do not run as a shared service without adding auth |
| GGUF model size | 32B model requires 22 GB RAM | Smaller machines must use a 7B or 14B model |

---

## Troubleshooting

??? question "`ModuleNotFoundError: No module named 'backend'`"
    You are running `uvicorn` from inside the `backend/` folder. Run it from the **repo root**:
    ```bash
    cd phil-knowledge-navigator  # make sure you're here
    uvicorn backend.main:app --reload --port 8001
    ```

??? question "`ChromaDB SIGBUS error` or `mmap error`"
    ChromaDB uses memory-mapped files. These **must not** live on a network drive, OneDrive, Dropbox, or iCloud folder. Phil stores them at `/tmp/phil_chroma` by default — this is intentional. Do not move the database to a synced folder.

??? question "Mail / calendar returns empty"
    1. Check `backend/.env` — verify `GOG_ACCOUNT` and `GOG_KEYRING_PASSWORD` are correct.
    2. Test the API directly: open `http://localhost:8001/api/mails` in your browser. You should see JSON.
    3. For Google Calendar: verify `GOG_ACCOUNT` is set and run `gog calendar events --account you@gmail.com --max 3` to test the CLI directly.
    4. For Exchange: check your login credentials — click the account icon in the sidebar to re-enter them.

??? question "`ANTHROPIC_API_KEY` error / 401 Unauthorized"
    Your key is either missing, incorrect, or has no credits. Check [console.anthropic.com](https://console.anthropic.com) → usage. The key must start with `sk-ant-`.

??? question "LM Studio returns timeout / local LLM not responding"
    1. Open LM Studio → **Local Server** tab → confirm "Running" is shown.
    2. Test: `curl http://localhost:1234/v1/models` should return JSON.
    3. Check that `LOCAL_LLM_ENDPOINT` and `LOCAL_LLM_MODEL` are correctly set in `backend/.env`.

??? question "Frontend shows blank page or cannot reach backend"
    Confirm both servers are running: backend on port **8001**, frontend on port 5173. The frontend proxies API requests to the backend — if the backend is down, the frontend will show network errors in the browser console (F12).

??? question "I don't have a Google account — can I use Phil?"
    Yes. Log in with your Exchange credentials (THWS or Microsoft 365) on the login screen. Calendar events will come from Exchange EWS. Or use demo mode and skip the login.

??? question "`gog: command not found`"
    The `gog` binary is not installed or not in your `$PATH`. Install it with Homebrew (`brew install nicholasgasior/tap/gog`) or download the binary from [github.com/nicholasgasior/gog/releases](https://github.com/nicholasgasior/gog/releases) and place it in `~/bin/` or `/usr/local/bin/`.

??? question "Google Calendar shows empty / `gog calendar: empty calendarId`"
    Set `GOG_ACCOUNT` in `backend/.env` to your full Gmail address. Then restart the backend (`Ctrl+C` and re-run `uvicorn ...`). Phil reads `.env` at startup — changes do not hot-reload automatically.

---

## Install helpers

=== "macOS"

    ```bash
    # Install Homebrew (package manager for macOS)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Then install Python and Node
    brew install python@3.12 node git
    ```

=== "Windows"

    1. Python: [python.org/downloads](https://www.python.org/downloads/) → Download Python 3.12 → check "Add Python to PATH" during install
    2. Node.js: [nodejs.org](https://nodejs.org/) → Download LTS version
    3. Git: [git-scm.com](https://git-scm.com/download/win)

=== "Linux (Ubuntu / Debian)"

    ```bash
    sudo apt update
    sudo apt install python3.12 python3.12-venv python3-pip nodejs npm git
    ```

=== "Linux (Fedora / RHEL)"

    ```bash
    sudo dnf install python3.12 nodejs npm git
    ```

---

## Maintenance

### Keeping Phil up to date

```bash
cd phil-knowledge-navigator
git pull

# Re-install backend dependencies (if requirements.txt changed)
source .venv/bin/activate
pip install -r backend/requirements.txt

# Re-install frontend dependencies (if package.json changed)
cd frontend && npm install && cd ..
```

For Docker: `docker compose -f docker-compose.local.yml up --build` automatically rebuilds on every start.

### Data directories

Phil stores persistent data in two locations:

| Path | What it contains | Important notes |
|------|-----------------|-----------------|
| `/tmp/phil_chroma` | ChromaDB — email embeddings for RAG | **Must be on local disk** (not OneDrive/Dropbox). Cleared on reboot on macOS/Linux. |
| `/data/memory.db` (Docker) or `./memory.db` (dev) | SQLite — facts Phil has learned from conversations | Persists across restarts. Back this up if you want to keep your memory. |

To clear the knowledge base (e.g. after a major data change):

```bash
rm -rf /tmp/phil_chroma
# Then triage your mails again in the app to re-populate
```

To clear Phil's memory (start fresh):

```bash
rm memory.db           # dev
# or in Docker: docker compose exec kn-mail rm /data/memory.db
```

### Log access

=== "Dev mode"

    Backend logs appear in the terminal where you ran `uvicorn`. Frontend build/HMR messages appear in the npm terminal.

=== "Docker"

    ```bash
    # Follow live logs
    docker compose logs -f

    # Last 100 lines
    docker compose logs --tail=100
    ```

### Rotating API keys

If you need to replace an API key:

1. Generate the new key in [console.anthropic.com](https://console.anthropic.com) or [platform.openai.com](https://platform.openai.com)
2. Update `backend/.env`
3. Restart the backend: `Ctrl+C` → `uvicorn backend.main:app --reload --port 8001`
4. Revoke the old key in the provider console

### Re-authenticating Google Calendar

If `gog auth login` needs to be re-run (token expired or revoked):

```bash
gog auth logout
gog auth login
```

The new token is stored in the system keyring automatically. No changes to `.env` needed.

For Docker: export the new `GOG_KEYRING_PASSWORD` and restart the container.

### Production deployment (Traefik)

The production `docker-compose.yml` includes Traefik labels for automatic HTTPS via Let's Encrypt.
Requirements:

- A domain name pointing to your server (A record)
- Traefik running on the same Docker network (`traefik-net`)
- A Let's Encrypt email configured in your Traefik config

```bash
# Deploy (production)
docker compose up -d

# Check status
docker compose ps
docker compose logs kn-mail
```

The app will be available at `https://kn-mail.yourdomain.com` (edit the host rule in `docker-compose.yml`).
