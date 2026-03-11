from __future__ import annotations

import json
from pathlib import Path
from typing import List


def write_srt(segments_meta_path: str, srt_path: str) -> None:
    meta = json.loads(Path(segments_meta_path).read_text())
    segments = meta.get("segments", [])
    lines = []
    for idx, seg in enumerate(segments, start=1):
        start_s = seg["start_offset_s"]
        end_s = seg["end_offset_s"]
        start = _format_srt_time(start_s)
        end = _format_srt_time(end_s)
        label = f"segment {seg['index']}"
        lines.append(str(idx))
        lines.append(f"{start} --> {end}")
        lines.append(label)
        lines.append("")
    Path(srt_path).write_text("\n".join(lines))


def _format_srt_time(seconds: float) -> str:
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def concatenate_wavs(segment_files: List[str], output_wav: str) -> None:
    import wave

    if not segment_files:
        return
    with wave.open(segment_files[0], "rb") as first:
        params = first.getparams()

    with wave.open(output_wav, "wb") as out:
        out.setparams(params)
        for path in segment_files:
            with wave.open(path, "rb") as wf:
                out.writeframes(wf.readframes(wf.getnframes()))
