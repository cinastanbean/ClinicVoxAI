from __future__ import annotations

import json
from pathlib import Path

from app.voice.audio_segments import concatenate_wavs, write_srt


def run() -> None:
    out_dir = Path("outputs")
    meta_files = sorted(out_dir.glob("twilio_out_*_segments.json"))
    if not meta_files:
        print("No segment metadata found in outputs/")
        return

    meta_path = meta_files[-1]
    meta = json.loads(meta_path.read_text())
    segments = meta.get("segments", [])
    segment_files = [seg["file"] for seg in segments]

    merged_wav = out_dir / meta_path.name.replace("_segments.json", "_merged.wav")
    srt_path = out_dir / meta_path.name.replace("_segments.json", ".srt")

    concatenate_wavs(segment_files, str(merged_wav))
    write_srt(str(meta_path), str(srt_path))

    print(f"Wrote {merged_wav}")
    print(f"Wrote {srt_path}")


if __name__ == "__main__":
    run()
