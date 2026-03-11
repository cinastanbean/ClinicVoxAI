from __future__ import annotations

import os
import websocket


def run() -> None:
    url = os.getenv("RETELL_WS_URL", "ws://127.0.0.1:8000/retell/stream")
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(b"\x00\x01\x02")
    ws.close()


if __name__ == "__main__":
    run()
