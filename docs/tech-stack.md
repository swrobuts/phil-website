# Tech Stack

## Backend

| Library | Version | Purpose |
|---------|---------|---------|
| FastAPI | ≥0.115 | Web framework + async API |
| Uvicorn | ≥0.30 | ASGI server |
| Anthropic SDK | ≥0.40 | Claude API client |
| OpenAI SDK | ≥1.40 | OpenAI + embedding client |
| exchangelib | ≥5.1 | Google Workspace EWS client |
| python-dotenv | ≥1.0 | `.env` configuration |
| httpx | ≥0.27 | Async HTTP client |
| ChromaDB | ≥0.5 | Vector store for RAG + memory |
| pdfplumber | ≥0.11 | PDF text extraction |
| python-docx | ≥1.1 | DOCX text extraction |
| rdflib | ≥7.0 | RDF/OWL ontology graph |
| pyhafas | ≥0.6 | Deutsche Bahn Hafas API client |
| pytest | ≥8.0 | Test framework |

## Frontend

| Library | Version | Purpose |
|---------|---------|---------|
| React | 18 | UI component framework |
| TypeScript | — | Type-safe JavaScript |
| Vite | — | Build tool + dev server |
| CSS Modules | — | Scoped component styles |

## Infrastructure

| Tool | Purpose |
|------|---------|
| Docker | Container image for production deployment |
| Traefik | Reverse proxy + TLS (production) |
| GitHub Actions | CI/CD — build & deploy this site |
| GitHub Pages | Hosting for this documentation |

## External Services

| Service | Purpose |
|---------|---------|
| Anthropic Claude API | LLM for chat, triage, briefing, fact extraction |
| Google Workspace | Gmail + Calendar via EWS protocol |
| DuckDuckGo | Web search (no API key required) |
| Deutsche Bahn Hafas | Train schedule queries via PyHafas |
