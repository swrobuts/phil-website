# Architecture

Phil is a single-service web application: a FastAPI backend that serves both
the React frontend (as static files) and a REST + SSE API.

## System Overview

```
Browser
  ↓  HTTP / EventSource
FastAPI (uvicorn)
  ├── /static → React SPA (built Vite bundle)
  ├── /api/mails → exchange_helpers.py → Google Workspace (EWS)
  ├── /api/calendar → exchange_helpers.py → Google Calendar (EWS)
  ├── /api/chat (SSE) → main.py → LLM client → Anthropic / OpenAI / Local LLM
  │                              → knowledge_store.py (ChromaDB RAG)
  │                              → ontology_store.py (RDFlib graph)
  │                              → memory_store.py (SQLite + ChromaDB)
  │                              → web_search.py (DuckDuckGo)
  ├── /api/triage-mails → main.py → LLM (COSTAR_PROMPT)
  │                               → attachment_extractor.py (PDF/DOCX)
  │                               → ontology_store.py (entity indexing)
  ├── /api/briefing (SSE) → main.py → LLM (BRIEFING_SYSTEM)
  │                                 → knowledge_store.py (RAG)
  └── /api/memory/* → memory_store.py (SQLite + ChromaDB)
```

## Backend Modules

| Module | Responsibility |
|--------|---------------|
| `main.py` | FastAPI app, all route handlers, prompt constants, business logic |
| `llm_client.py` | Hybrid LLM client: cloud (Anthropic/OpenAI) + local (LM Studio) with fallback |
| `exchange_helpers.py` | Google Workspace integration: mail fetch, calendar fetch |
| `knowledge_store.py` | ChromaDB vector store for email RAG |
| `ontology_store.py` | RDFlib RDF/OWL graph for entity relationships |
| `memory_store.py` | SQLite + ChromaDB dual-layer memory with RLHF |
| `attachment_extractor.py` | PDF (pdfplumber) + DOCX (python-docx) text extraction |
| `web_search.py` | DuckDuckGo search wrapper with trigger regex |

## Frontend Structure

```
frontend/src/
  components/
    Views/
      Dashboard.tsx      ← main overview with event context panel
      MailsView.tsx      ← mail triage list
      CalendarView.tsx   ← calendar grid
      TasksView.tsx      ← task list
      MemoryView.tsx     ← fact browser with edit/delete
      TrainView.tsx      ← RLHF training interface
    Phil/                ← chat component with streaming
    Cards/               ← reusable mail/event cards
    Layout/              ← sidebar, nav, badges
```

## Data Flow: Mail Triage

```
POST /api/triage-mails
  → exchange_helpers.fetch_google_mails()
  → For each mail:
      → attachment_extractor (if attachments)
      → LLM.create(COSTAR_PROMPT) → JSON result
      → ontology_store.index_mail_entities()
      → knowledge_store.add_mail() (ChromaDB embedding)
  → Return sorted list
```

## Data Flow: Chat

```
POST /api/chat  (streaming SSE)
  → _build_context(message)
      → fetch_google_calendar() [if calendar keywords detected]
      → knowledge_store.search() [RAG — top 3 similar mails]
      → ontology_store.get_context_for_chat()
      → memory_store.search_facts() [top 5 relevant facts]
      → web_search() [if trigger regex matches]
  → LLM.stream(PHIL_SYSTEM, full_context + user_message)
  → Stream tokens to frontend via SSE
  → [background] _extract_and_store_facts()
```
