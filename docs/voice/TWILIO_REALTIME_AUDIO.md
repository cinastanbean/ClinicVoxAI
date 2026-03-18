# Twilio Realtime Audio Controls

## Denoise (Soft Gate)
- `apply_soft_gate` drops very low-energy frames to reduce noise.
- Placeholder for real DSP.

## Length Limit
- `max_utterance_s` forces commit + response after a duration.

## Adaptive VAD
- `idle_flush_s` adapts to silence gaps using EMA.
- Clamp range: 0.3s to 1.2s.

## Output WAV
- Output audio returned to Twilio is saved locally as WAV segments in `outputs/`.
- Metadata JSON includes timestamped segment markers.
