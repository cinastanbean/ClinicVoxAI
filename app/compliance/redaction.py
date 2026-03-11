from __future__ import annotations

import re


def redact_phi(text: str) -> str:
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "[REDACTED_DOB]", text)
    text = re.sub(r"\+1\d{10}", "[REDACTED_PHONE]", text)
    return text
