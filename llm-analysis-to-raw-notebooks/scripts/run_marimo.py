#!/usr/bin/env python3
"""Execute marimo lessons headlessly through static HTML export and log validation.

Usage: python scripts/run_marimo.py lesson.py --data-root DIR --output-root DIR
             [--full-cohort] [--timeout SECONDS]
This tests execution, not interactive controls or scientific correctness.
Requires marimo already installed; never installs dependencies or downloads data.
"""
import argparse
import importlib.metadata as md
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("notebook")
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--full-cohort", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()
    notebook = Path(a.notebook).expanduser().resolve()
    data = Path(a.data_root).expanduser().resolve()
    out = Path(a.output_root).expanduser().resolve()
    if not notebook.is_file() or not data.is_dir():
        sys.exit("Notebook file or DATA_ROOT directory unavailable")
    if out == data or data in out.parents:
        sys.exit("OUTPUT_ROOT must be separate from DATA_ROOT")
    try:
        marimo_ver = md.version("marimo")
    except md.PackageNotFoundError:
        sys.exit("Missing marimo dependency; install it in the environment before validation")
    ex = out / "executed"
    ex.mkdir(parents=True, exist_ok=True)
    html = ex / (notebook.stem + ".html")
    env = dict(os.environ, DATA_ROOT=str(data), OUTPUT_ROOT=str(out),
               RUN_FULL_COHORT="1" if a.full_cohort else "0")
    # No shell interpolation. Export runs the marimo notebook: only execute trusted reviewed inputs.
    cmd = [sys.executable, "-m", "marimo", "export", "html",
           str(notebook), "-o", str(html)]
    started = time.monotonic()
    error = None
    try:
        proc = subprocess.run(cmd, cwd=str(notebook.parent), env=env,
                              capture_output=True, text=True, timeout=a.timeout)
        if proc.returncode:
            error = {"type": "ExportError", "message": (proc.stderr or proc.stdout)[-1200:]}
    except subprocess.TimeoutExpired:
        error = {"type": "Timeout", "message": f"export exceeded {a.timeout}s"}
    elapsed = round(time.monotonic()-started, 1)
    rec = {"notebook": notebook.name, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
           "environment": {"python": platform.python_version(), "marimo": marimo_ver},
           "data_root_name": data.name, "full_cohort": a.full_cohort,
           "html": html.name if html.exists() and error is None else None,
           "runtime_seconds": elapsed, "error": error, "headless_succeeded": error is None,
           "interactive_controls_tested": False, "scientific_comparison_verified": False,
           "reminder": "Inspect executed results, compare every source output, and test optional widgets separately."}
    record = ex / (notebook.stem + ".validation.json")
    record.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(json.dumps({"headless_succeeded": rec["headless_succeeded"], "record": str(record)}))
    return 0 if error is None else 1

if __name__ == "__main__":
    sys.exit(main())
