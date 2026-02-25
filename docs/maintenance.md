# Maintenance

## Keeping Phil up to date

=== "Docker Hub (Option A)"

    ```bash
    docker pull swrobuts/phil:latest
    docker stop phil && docker rm phil
    docker run -d --name phil -p 8000:8000 --env-file backend.env swrobuts/phil:latest
    ```

=== "Docker Compose (Option B)"

    ```bash
    git pull
    docker compose -f docker-compose.local.yml up --build
    ```

=== "Dev mode (Option C)"

    ```bash
    cd phil-knowledge-navigator
    git pull

    source .venv/bin/activate
    pip install -r backend/requirements.txt

    cd frontend && npm install && cd ..
    ```

---

## Data directories

Phil stores persistent data in two locations. Both are on the local machine only — no data is synced to a cloud service by Phil itself.

| Path | What it contains | Notes |
|------|-----------------|-------|
| `/tmp/phil_chroma` | ChromaDB — email embeddings (RAG) | **Local disk only.** `/tmp` is cleared on reboot on Linux/macOS. Move to a stable path if you need persistence across reboots. |
| `./memory.db` (dev) / `/data/memory.db` (Docker) | SQLite — facts Phil has learned | Persists across restarts. Back this up to keep your memory. |

### Move ChromaDB to a stable path

To survive reboots, move the ChromaDB directory and symlink it, or set a different path. The path is currently hardcoded to `/tmp/phil_chroma` in `backend/knowledge_store.py` and `backend/memory_store.py`. Edit these files to change it, then restart the backend.

!!! warning "Never put ChromaDB on a network drive"
    OneDrive, iCloud, Dropbox, and similar sync folders use POSIX file locking that is incompatible with ChromaDB's memory-mapped files. Placing the database there causes `SIGBUS` errors. Use a local SSD path only.

---

## Clearing the knowledge base

After a major inbox change or when re-indexing is needed:

```bash
rm -rf /tmp/phil_chroma
```

Then open the Mail view and click **Analysieren** to re-populate. Each triage run embeds the fetched emails.

---

## Clearing Phil's memory

To reset all facts Phil has learned from conversations:

```bash
# Dev
rm memory.db

# Docker
docker compose exec kn-mail rm /data/memory.db
docker compose restart kn-mail
```

---

## Log access

=== "Dev mode"

    Backend logs appear in the terminal where you ran `uvicorn`. Set `LOG_LEVEL=debug` as an env var for more verbose output.

    Frontend HMR and build messages appear in the second terminal (npm).

=== "Docker"

    ```bash
    # Follow live logs
    docker compose logs -f kn-mail

    # Last 200 lines
    docker compose logs --tail=200 kn-mail

    # Filter by level (all ERROR lines)
    docker compose logs kn-mail 2>&1 | grep ERROR
    ```

---

## Rotating API keys

If an API key is compromised or expires:

1. Generate a replacement key in the provider console:
    - Anthropic: [console.anthropic.com](https://console.anthropic.com) → API Keys
    - OpenAI: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Update `backend/.env`
3. Restart the backend (`Ctrl+C` → `uvicorn backend.main:app --reload --port 8001`, or `docker compose restart kn-mail`)
4. Revoke the old key in the provider console

---

## Re-authenticating Google Calendar (`gog`)

OAuth tokens eventually expire or need to be refreshed after a Google security event.

```bash
gog auth logout
gog auth login   # opens browser for re-auth
```

The new token is stored in the system keyring automatically. `GOG_ACCOUNT` in `.env` does not need to change.

**Docker:** If the token was refreshed, export the new `GOG_KEYRING_PASSWORD` and restart the container.

---

## Backing up

A minimal backup covers:

| What | Where | How |
|------|-------|-----|
| Config | `backend/.env` | Copy to a password manager or encrypted USB — **never to git** |
| Memory | `memory.db` | `cp memory.db memory.db.bak` (or automated daily copy) |
| Knowledge base | `/tmp/phil_chroma/` | `cp -r /tmp/phil_chroma ~/phil_chroma_backup` (optional — can always be re-built from mails) |

The source code itself is in git — no backup needed beyond `git push`.

---

## Production deployment (Traefik + Let's Encrypt)

`docker-compose.yml` includes Traefik labels for automatic HTTPS.

### Requirements

- A server with a public IP and a domain name pointing to it (A record)
- [Traefik](https://traefik.io) running as a Docker service on the same `traefik-net` network
- Let's Encrypt email configured in your Traefik static config

### Steps

```bash
# Confirm traefik-net exists
docker network ls | grep traefik-net

# Edit docker-compose.yml — replace the host rule:
#   traefik.http.routers.kn-mail.rule=Host(`kn-mail.yourdomain.com`)

# Deploy
docker compose up -d

# Verify
docker compose ps
curl https://kn-mail.yourdomain.com/health
```

Expected response from `/health`:

```json
{"status": "ok"}
```

### Updating in production

```bash
git pull
docker compose up -d --build
```

This rebuilds the image and restarts the container with zero manual steps. The `restart: unless-stopped` policy ensures the container comes back after server reboots.

---

## Uninstalling Phil

```bash
# Stop and remove containers
docker compose down --volumes

# Remove the image
docker rmi kn-mail

# Remove data
rm -rf /tmp/phil_chroma
rm memory.db

# Remove the repo
rm -rf phil-knowledge-navigator
```

The `gog` keyring entry can be removed with `gog auth logout`.
