from __future__ import annotations

import base64
from typing import Optional


def apply_soft_gate(payload_b64: str, min_energy: int = 4) -> Optional[str]:
    """
    Very light 'denoise' gate: if max byte energy is below threshold, drop frame.
    Note: This is a placeholder for real DSP. Works on g711_ulaw bytes.
    """
    try:
        raw = base64.b64decode(payload_b64)
    except Exception:
        return payload_b64
    if not raw:
        return None
    peak = max(raw)
    if peak < min_energy:
        return None
    return payload_b64
