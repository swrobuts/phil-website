# Speech Output

Phil reads briefings and responses aloud using the **OpenAI Text-to-Speech API** — natural, high-quality voice synthesis streamed directly to the browser.

## How it works

1. You click the **🔊** button on any Phil response in the chat panel.
2. The frontend sends the response text to the backend (`/api/tts`).
3. The backend calls the OpenAI TTS API (`tts-1` or `tts-1-hd` model) and streams the audio back as an MP3.
4. The browser plays the audio in-line — no page reload, no file download.

## Why OpenAI TTS

Phil uses the OpenAI TTS API rather than browser-native speech synthesis (`speechSynthesis`) for quality reasons. Browser synthesis voices sound robotic and vary significantly by OS and browser. OpenAI TTS produces natural, expressive speech that makes listening to AI-generated briefings genuinely pleasant.

The trade-off: `OPENAI_API_KEY` is required for this feature. Without it, the TTS button is silently disabled — all other Phil features continue to work normally.

## Required configuration

```bash
# backend/.env
OPENAI_API_KEY=sk-proj-...
```

See the [setup guide](../setup.md) for how to obtain an OpenAI API key.

## Cost

OpenAI TTS pricing (as of early 2026): roughly **$0.015 per 1,000 characters** (`tts-1`), or **$0.030** for `tts-1-hd`. A typical Phil briefing (200–400 characters) costs a fraction of a cent. Monthly costs for daily use are negligible.

## Privacy note

When TTS is triggered, the response text is sent to OpenAI's servers for synthesis. This is the same data-privacy consideration as using the Anthropic API for LLM requests — avoid sending sensitive content if you are operating under strict DSGVO constraints. For fully private deployments, simply omit `OPENAI_API_KEY` and the feature is disabled.

## Use cases

- **Morning briefing** — ask Phil to summarise your day, then listen while making coffee
- **Hands-free triage** — Phil reads out mail summaries while you commute
- **Meeting prep** — listen to Phil's briefing for your next appointment without looking at the screen
