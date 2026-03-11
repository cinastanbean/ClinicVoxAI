# Full Flow With Mocks

This demo uses mock telephony/STT/TTS/LLM and SQLite-backed stores to illustrate the full pipeline without real integrations.

## Components
- Telephony: `app/voice/telephony.py`
- STT: `app/voice/stt.py`
- TTS: `app/voice/tts.py`
- LLM: `app/llm/mock.py`
- DB: `app/tools/db_sqlite.py`
- Calendar: `app/tools/calendar_sqlite.py`
- Report store: `app/tools/report_store.py`
- Audit + redaction: `app/compliance/audit.py`, `app/compliance/redaction.py`

## Run (No Voice)
```bash
python scripts/demo_end_to_end_no_voice.py
```
