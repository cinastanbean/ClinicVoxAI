from __future__ import annotations

import os
import subprocess


def run() -> None:
    scripts = [
        "scripts/demo_call.py",
        "scripts/demo_intent_switch.py",
        "scripts/demo_verification_failure.py",
        "scripts/demo_handoff.py",
        "scripts/demo_full_flow.py",
        "scripts/demo_parallel_branch.py",
        "scripts/demo_conflict.py",
        "scripts/export_events.py",
        "scripts/render_trace_html.py",
        "scripts/render_trace_swimlane.py",
        "scripts/render_trace_timeline.py",
        "scripts/render_collab_summary.py",
        "scripts/generate_demo_report.py",
        "scripts/render_trace_screenshots.py",
    ]

    env = {**os.environ, "PYTHONPATH": "."}
    for script in scripts:
        print("=" * 80)
        print("Running:", script)
        subprocess.run(["python", script], check=False, env=env)


if __name__ == "__main__":
    run()
