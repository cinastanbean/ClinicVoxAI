from __future__ import annotations

import json
import os
import time

import websocket


def run() -> None:
    url = os.getenv("TWILIO_WS_URL", "ws://127.0.0.1:8000/twilio/stream")
    ws = websocket.WebSocket()
    ws.connect(url)

    ws.send(json.dumps({"event": "connected"}))
    ws.send(json.dumps({"event": "start", "start": {"streamSid": "S1"}}))
    time.sleep(0.1)
    ws.send(json.dumps({"event": "media", "media": {"payload": ""}}))
    time.sleep(0.1)
    ws.send(json.dumps({"event": "stop"}))
    ws.close()


if __name__ == "__main__":
    run()
