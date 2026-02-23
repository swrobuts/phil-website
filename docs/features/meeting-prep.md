# Meeting Preparation

Before any calendar event, Phil can prepare a structured briefing.

## What the briefing contains

```
## 👤 Participants
Names extracted from the event title and description

## 📬 Recent Mails
Emails related to the meeting (retrieved via RAG, similarity ≥ 60%)

## 📋 Agenda Suggestion
3–5 concrete points based on the event and related correspondence
```

## How it works

1. Phil parses the event title to extract person names (regex pattern `mit [Name]`)
2. A RAG query searches past emails for relevant correspondence
3. The result is sent to Claude with the `BRIEFING_SYSTEM` prompt
4. Response streams back to the UI in real time (Server-Sent Events)

## Trigger

Click the calendar event in the Dashboard or Calendar view → "Prepare Briefing" button.

!!! note "DE"
    Vor jedem Termin bereitet Phil ein kompaktes Briefing vor:
    Wer kommt? Welche Mails gab es zuletzt? Was sollte auf die Agenda?
