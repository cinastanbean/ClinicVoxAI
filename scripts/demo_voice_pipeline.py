from __future__ import annotations

from app.compliance.audit import AuditLogger
from app.graph.orchestrator import Orchestrator
from app.voice.telephony import TelephonyGateway
from app.voice.stt import STTClient
from app.voice.tts import TTSClient


def run() -> None:
    orch = Orchestrator()
    stt = STTClient()
    tts = TTSClient()
    audit = AuditLogger()

    def on_audio(event):
        transcript = stt.transcribe(event.audio_chunks)
        state = orch.new_state(event.session_id, caller_phone=event.caller_phone)
        for text in transcript:
            result = orch.handle_turn(state, text)
            audio_out = tts.synthesize(result["response"])
            audit.write("turn", {"text": text, "response": result["response"]})
            print("TTS:", audio_out)

    gateway = TelephonyGateway(on_audio=on_audio)
    gateway.simulate_call(
        session_id="VOICE-1",
        caller_phone="+15550000000",
        audio_chunks=[
            "I want to schedule an appointment",
            "My first name is Jane",
            "My last name is Doe",
            "My date of birth is 1990-01-01",
            "Wednesday morning works",
        ],
    )


if __name__ == "__main__":
    run()
