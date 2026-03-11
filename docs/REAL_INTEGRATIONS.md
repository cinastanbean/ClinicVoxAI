# Real Integrations (Scaffold)

## Twilio/Retell
- Webhook endpoint should call your Orchestrator
- Twilio expects TwiML XML response

## OpenAI
- LLM routing and report summarization: `app/llm/openai_client.py`
- STT: `app/voice/openai_stt.py`
- TTS: `app/voice/openai_tts.py`

## SQLAlchemy Storage
- DB: `app/tools/db_sqlalchemy.py`
- Calendar: `app/tools/calendar_sqlalchemy.py`
- Report: `app/tools/report_sqlalchemy.py`

Use `CONFIG.storage_backend = "sqlalchemy"` to enable.
