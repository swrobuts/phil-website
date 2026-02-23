# Calendar

Phil integrates with Google Calendar via the `exchangelib` library,
fetching up to 365 days ahead and 180 days back.

## Natural-language queries

Ask Phil in the chat:

- *"What's on next Tuesday?"*
- *"When is the faculty board meeting?"*
- *"Do I have anything with [name] this week?"*

Phil detects calendar-related keywords (`_calendar_keywords()` in `main.py`),
fetches your full calendar context, and answers from that context rather than
generating plausible-sounding (but potentially wrong) dates.

## Anti-hallucination design

A dedicated `KALENDERSUCHE` block in the context prompt is marked as authoritative.
If Phil's answer contradicts the data in this block, it must defer to the data.
This prevents the LLM from inventing appointments that don't exist.

!!! note "DE"
    Phil liest deinen Google-Kalender und beantwortet Fragen dazu.
    Halluzinationen werden durch einen expliziten Autoritätsblock im Prompt verhindert.
