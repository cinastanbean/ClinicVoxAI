from __future__ import annotations

import os
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app.graph.orchestrator import Orchestrator
from app.monitoring.health import check_health
from app.voice.stt import STTClient
from app.voice.tts import TTSClient
from app.voice.openai_stt import OpenAISTTClient
from app.voice.openai_tts import OpenAITTSClient
from app.voice.twilio_stream import TwilioStreamBridge
from app.voice.retell_stream import RetellStreamBridge

app = FastAPI(title="Voice AI Clinic Assistant")
orch = Orchestrator()
stt = STTClient()
tts = TTSClient()


class CallRequest(BaseModel):
    session_id: str
    caller_phone: str | None = None
    transcript: list[str]


class VoiceRequest(BaseModel):
    session_id: str
    caller_phone: str | None = None
    audio_chunks: list[str]


@app.get("/health")
def health() -> dict:
    status = check_health()
    return {"ok": status.ok, "details": status.details}


@app.post("/call/simulate")
def simulate_call(req: CallRequest) -> dict:
    return orch.simulate_call(req.transcript, req.session_id, req.caller_phone)


@app.post("/voice/mock")
def voice_mock(req: VoiceRequest) -> dict:
    transcript = stt.transcribe(req.audio_chunks)
    state = orch.new_state(req.session_id, req.caller_phone)
    responses = []
    for text in transcript:
        result = orch.handle_turn(state, text)
        responses.append(tts.synthesize(result["response"]))
    return {"responses": responses, "state": state}


@app.post("/stt/openai")
def stt_openai(file: UploadFile = File(...)) -> dict:
    client = OpenAISTTClient()
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(file.file.read())
    text = client.transcribe_file(tmp_path)
    return {"text": text}


@app.post("/tts/openai")
def tts_openai(req: CallRequest) -> dict:
    client = OpenAITTSClient()
    out_path = "/tmp/tts_output.mp3"
    client.synthesize_to_file(" ".join(req.transcript), out_path)
    return {"file": out_path}


@app.post("/twilio/voice", response_class=PlainTextResponse)
def twilio_voice() -> str:
    stream_url = os.getenv("TWILIO_STREAM_URL", "wss://example.com/ws/audio")
    twiml = f"""
<Response>
  <Say>Welcome to the clinic. Please hold while we connect you.</Say>
  <Start>
    <Stream url=\"{stream_url}\" />
  </Start>
</Response>
""".strip()
    return twiml


@app.websocket("/twilio/stream")
async def twilio_stream(websocket: WebSocket) -> None:
    bridge = TwilioStreamBridge(websocket)
    await bridge.handle()


@app.websocket("/retell/stream")
async def retell_stream(websocket: WebSocket) -> None:
    bridge = RetellStreamBridge(websocket)
    await bridge.handle()


@app.post("/retell/webhook")
def retell_webhook(payload: dict) -> dict:
    return {"status": "ok", "echo": payload}
