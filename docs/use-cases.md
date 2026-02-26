# Use Cases: 1987 vs. 2026

Apple's 1987 concept video demonstrated eight concrete use cases.
What was then pure fiction is now technically realisable — though not always by a single system.

This page maps each Apple use case to what exists in 2026, distinguishing clearly
between what **Phil implements directly** and what today's other tools provide.

---

| # | Apple 1987 | Phil 2026 | Other Tools |
|---|-----------|-----------|-------------|
| 1 | **Conversational AI Agent** — natural language dialogue, proactive suggestions | ✅ Phil Chat with streaming, context injection, proactive next steps | ChatGPT, Claude.ai |
| 2 | **Calendar Management** — scheduling, reminders, agenda | ✅ Calendar view, natural-language search, meeting briefings | Google Calendar, Siri |
| 3 | **Video Conferencing** — real-time video with colleague | — Not in Phil | Zoom, Teams, Google Meet |
| 4 | **Knowledge Research** — intelligent search in scientific databases | ✅ Semantic RAG search over emails + attachments | Perplexity, Semantic Scholar |
| 5 | **Data Visualisation** — interactive charts, geographic simulations | ✅ Live Rainforest Dashboard at [rainforest.butscher.cloud](https://rainforest.butscher.cloud) — real INPE PRODES data, KPI cards, animated treemap, choropleth map, deforestation simulation | ChatGPT Code Interpreter, Plotly |
| 6 | **Document Summarisation** — briefing from papers and messages | ✅ Mail summaries, attachment extraction, meeting prep briefings | NotebookLM, Claude |
| 7 | **Simulation** — complex scenario modelling | — Not in Phil | Specialist tools |
| 8 | **Multimodal Interaction** — touch, voice, gesture | — Web UI only; no voice input | Siri, Alexa, Google Assistant |

---

## What Phil Does Well

Phil focuses on the daily information management problem that the 1987 video showed in its
opening minutes: managing the flow of messages, understanding what needs attention,
and preparing for the day ahead.

- **Mail triage** — categorise, prioritise, summarise, recommend actions (UC 1, 2, 6)
- **Calendar awareness** — understand what is coming and why it matters (UC 2)
- **Meeting preparation** — briefing a user before a meeting using past correspondence (UC 4, 6)
- **Memory** — learning facts about the user's world across sessions (UC 1)
- **RAG search** — finding relevant past emails semantically (UC 4)

## What Phil Does Not Do (and why)

Phil does not implement video conferencing (UC 3), complex simulation (UC 7) or voice input (UC 8).
This is not a shortcoming — it is a scope decision.
These are better served by dedicated tools. Phil's value is in the daily information layer.

!!! note "DE — Für Studierende"
    Phil ist kein Alleskönner. Jede Funktion wurde bewusst ausgewählt: Was bringt den
    größten Mehrwert im Hochschulalltag? Die Use Cases 3, 7, 8 sind im Vortrag
    konzeptuelle Parallelen (Zoom für UC3, Perplexity für UC4 usw.) — nicht Ziele für Phil selbst.
    UC 5 (Datenvisualisierung) ist durch das eigenständige Rainforest Dashboard unter
    rainforest.butscher.cloud abgedeckt.
