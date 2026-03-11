# Realtime Streaming (OpenAI)

## Twilio Media Streams
- Twilio sends JSON frames with `event=media` and a base64 audio `payload`.
- We forward payloads to OpenAI Realtime as `input_audio_buffer.append`.

## Retell Stream
- This stub accepts raw audio bytes over WebSocket and forwards to OpenAI.

## Notes
- Requires `OPENAI_API_KEY`
- See OpenAI Realtime guide for event schema.
