#!/usr/bin/env python3
"""Static portability checks for native marimo lesson files; optionally run marimo check.

Usage: python scripts/check_marimo.py NOTEBOOK.py [MORE.py ...] [--json]
Requires only stdlib for static checks. marimo CLI lint is run if available and
reported separately; missing marimo is a warning, never a false DAG pass.
"""
import ast
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ABS_PATH = re.compile(r"""["'](/Users/|/home/|/mnt/|/Volumes/|/scratch/|/data/|[A-Za-z]:\\)""")
INSTALL = re.compile(r"\bpip\s+install\b|\bconda\s+install\b|\bsubprocess\.(run|Popen)\([^)]*(pip|conda)", re.I)
NETWORK = re.compile(r"\brequests\.(get|post)\b|\bhttpx\.|\burllib\.request\b|\b(urlretrieve|wget|curl)\b|openneuro\.download")
def check(path):
    errors, warnings = [], []
    try:
        source = Path(path).read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, SyntaxError) as exc:
        return [str(exc)], [], "not_run"
    if "marimo.App(" not in source or "@app.cell" not in source:
        errors.append("not a native marimo.App with @app.cell definitions")
    if "DATA_ROOT" not in source or "OUTPUT_ROOT" not in source:
        errors.append("missing configurable DATA_ROOT or OUTPUT_ROOT")
    if ABS_PATH.search(source):
        errors.append("hard-coded absolute data path")
    if INSTALL.search(source):
        errors.append("package installation command in notebook")
    if NETWORK.search(source):
        errors.append("network retrieval in offline teaching notebook")
    if "Student checkpoint" not in source and "student checkpoint" not in source.lower():
        warnings.append("no student prediction/inspection checkpoint")
    if "source" not in source.lower() or "comparison" not in source.lower():
        warnings.append("no source-versus-student comparison")
    if "sensitivity" not in source.lower():
        warnings.append("no deterministic sensitivity pathway described")
    if "interactivity" in source.lower() and "optional" not in source.lower() and "offer" not in source.lower():
        warnings.append("check that controls are optional, not necessary for reproduction")
    # Check isn't proof of meaningful scientific validity. DAG lint needs marimo itself.
    dag = "unavailable"
    if importlib.util.find_spec("marimo") is not None:
        try:
            run = subprocess.run([sys.executable, "-m", "marimo", "check", str(path)],
                                 capture_output=True, text=True, timeout=90)
            dag = "passed" if run.returncode == 0 else "failed"
            if run.returncode:
                errors.append("marimo dependency/format check failed: " + (run.stderr or run.stdout)[-700:])
        except (OSError, subprocess.TimeoutExpired) as exc:
            dag = "unavailable"
            warnings.append(f"marimo check unavailable: {exc}")
    else:
        warnings.append("marimo not installed; dependency graph not validated")
    return errors, warnings, dag

def main(argv):
    as_json = "--json" in argv
    paths = [x for x in argv if x != "--json"]
    if not paths:
        print(__doc__)
        return 2
    result = {}
    for path in paths:
        errors, warnings, dag = check(path)
        result[path] = {"errors": errors, "warnings": warnings, "dag_check": dag}
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        for path, r in result.items():
            print(("FAIL" if r["errors"] else "ok") + " " + path + " (DAG: " + r["dag_check"] + ")")
            for x in r["errors"]:
                print("  ERROR " + x)
            for x in r["warnings"]:
                print("  warning " + x)
    return int(any(v["errors"] for v in result.values()))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
