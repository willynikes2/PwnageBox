#!/usr/bin/env python3

import subprocess
from pathlib import Path

PROJECT_DIR = Path.cwd()
CONTEXT_FILE = PROJECT_DIR / "pwnagebox-spec.md"

GOAL = """Generate the full PwnageBox project from spec. Include AI modules (scammer, researcher, pwner, voicepwner), FastAPI backend, Dockerfile, pyproject.toml, SQLite integration, README.md, and tests folder. Use # File: headers for each file. Use Context7 for accurate up-to-date examples."""

def run_codex():
    cmd = [
        "codex",
        "--cd", str(PROJECT_DIR),
        "--goal", GOAL,
        "--context", str(CONTEXT_FILE),
        "--tool", "context7"
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

if __name__ == "__main__":
    run_codex()
