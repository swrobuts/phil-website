# Memory & Learning

Phil remembers facts about your world across sessions.

## How memory works

After each chat exchange, Phil extracts up to 3 new facts using the
`FACT_EXTRACTION_SYSTEM` prompt. Facts are stored in two layers:

1. **SQLite** — structured storage: `fact_id`, `text`, `category`, `confidence`, `source_ref`
2. **ChromaDB** — vector embeddings for semantic similarity search

## Categories

`Person` · `Projekt` · `Konzept` · `Prozedur` · `Ort`

## RLHF feedback

Every Phil chat bubble has a 👍 / 👎 button. Thumbs up increases confidence;
thumbs down decreases it. Facts below a confidence threshold are suppressed
from context injection.

## Memory view

The Memory tab shows all stored facts with:

- Confidence bar (visual)
- Category badge
- Source message reference
- Edit / Delete controls
- Filter by category

## Context injection

At chat time, the top-5 most relevant facts (by semantic similarity to the user's
question) are injected into the context as a `MEMORY` block before Phil responds.

!!! note "DE"
    Phil merkt sich Fakten aus euren Gesprächen (Personen, Projekte, Zusammenhänge)
    und nutzt sie beim nächsten Mal als Kontext. Daumen hoch/runter steuert das Lernen.
