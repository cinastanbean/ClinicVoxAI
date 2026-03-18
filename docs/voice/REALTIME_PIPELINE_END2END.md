# Realtime End-to-End Pipeline

## Flow
1. Twilio Media Stream sends g711_ulaw audio frames (base64)
2. `WS /twilio/stream` receives frames and forwards to OpenAI Realtime
3. OpenAI Realtime emits audio deltas (g711_ulaw)
4. Bridge sends deltas back to Twilio as `media` events with `streamSid`

## Flow Control
- Idle flush commits audio buffer if no media is received for a short window
- Output queue drops oldest packets and emits `clear` when needed

## Notes
- Ensure Realtime session uses `input_audio_format` and `output_audio_format` set to `g711_ulaw`
- Requires `OPENAI_API_KEY`
