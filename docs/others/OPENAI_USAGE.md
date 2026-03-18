# OpenAI Usage (Scaffold)

## Requirements
- Set `OPENAI_API_KEY`

## Config
- `CONFIG.router_backend = "openai"` to use OpenAI for intent routing
- `CONFIG.use_openai_llm = True` to use OpenAI for report summaries

## LLM
- `app/llm/openai_client.py`

## STT
- `app/voice/openai_stt.py`

## TTS
- `app/voice/openai_tts.py`

## Demo
```bash
python scripts/demo_openai_stub.py
```
