# Mail Triage

Phil's core feature: read your inbox and decide what matters.

## How it works

1. Phil fetches emails from Google Workspace via the Exchange protocol
2. Each email is analysed by Claude using the CO-STAR triage prompt
3. A category, priority score, 2-sentence summary, and recommended action are returned
4. Results appear in the Mail view, sorted by priority

## Categories

| Category | Priority | When |
|----------|----------|------|
| VIP | 1 | Deanery, superiors, important partners |
| Action Required | 2 | Students, colleagues with concrete requests |
| FYI | 3 | Newsletters, informational only |
| Noise | 4 | Spam, advertising, irrelevant |

## Attachment extraction

If an email has attachments (PDF, DOCX), Phil extracts the text and includes
a 3-sentence summary in the triage result. Powered by `pdfplumber` and `python-docx`.

## Sentiment analysis

Each email also receives a sentiment score from -1.0 (very negative) to +1.0 (very positive).
This appears as a colour-coded indicator on the mail card.

## API endpoint

`POST /api/triage-mails` — fetches recent mails, runs triage, returns categorised results.

!!! note "DE"
    Phil liest deine E-Mails, kategorisiert sie nach Priorität und fasst jede in zwei Sätzen zusammen.
    Du siehst in 5 Sekunden, was sofortige Aufmerksamkeit braucht.
