# Twilio Media Streams (Scaffold)

## Server Endpoints
- `POST /twilio/voice` returns TwiML with <Stream>
- `WS /twilio/stream` receives JSON frames

## Events
- `connected`, `start`, `media`, `stop`, `clear`

## Notes
- We capture `streamSid` from `start` and include it in outbound `media` responses.
- When output buffer is full, a `clear` event is sent to reduce latency.

## Simulation
```bash
python scripts/demo_twilio_stream_sim.py
```
