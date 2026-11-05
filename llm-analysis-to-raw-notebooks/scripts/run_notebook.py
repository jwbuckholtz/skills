#!/usr/bin/env python3
"""Execute a teaching notebook headlessly and write a JSON validation record.

Usage:
  python run_notebook.py NOTEBOOK.ipynb --data-root DIR --output-root DIR
                         [--full-cohort] [--timeout SECONDS] [--kernel NAME]

The source notebook is never modified. The executed copy goes to
OUTPUT_ROOT/executed/<name>.ipynb and the record to
OUTPUT_ROOT/executed/<name>.validation.json.

Requires nbformat, nbclient and a Jupyter kernel to be installed already;
this script reports what is missing and does not install anything.
"""
import argparse
import importlib.metadata as md
import json
import os
import platform
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

KEY_PACKAGES = [
    "numpy", "scipy", "pandas", "matplotlib", "scikit-learn", "statsmodels",
    "mne", "mne-bids", "nibabel", "nilearn", "dipy", "neo", "elephant", "pynwb", "h5py", "xarray",
]


def versions():
    out = {}
    for name in KEY_PACKAGES:
        try:
            out[name] = md.version(name)
        except md.PackageNotFoundError:
            pass
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notebook")
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--full-cohort", action="store_true", help="sets RUN_FULL_COHORT=1 (deliberate full run)")
    ap.add_argument("--timeout", type=int, default=1800, help="per-cell timeout in seconds")
    ap.add_argument("--kernel", default="python3")
    a = ap.parse_args()

    try:
        import nbformat
        from nbclient import NotebookClient
        from nbclient.exceptions import CellExecutionError, CellTimeoutError
    except ImportError as exc:
        sys.exit(f"Missing dependency: {exc.name}. Install nbformat, nbclient and ipykernel in this environment first.")

    nb_path = Path(a.notebook)
    data_root = Path(a.data_root).expanduser()
    out_root = Path(a.output_root).expanduser()
    if not data_root.is_dir():
        sys.exit(f"DATA_ROOT is not a directory: {data_root}")
    try:
        out_root.resolve().relative_to(data_root.resolve())
        sys.exit("OUTPUT_ROOT is inside DATA_ROOT; keep generated files separate from raw data.")
    except ValueError:
        pass
    exec_dir = out_root / "executed"
    exec_dir.mkdir(parents=True, exist_ok=True)

    os.environ["DATA_ROOT"] = str(data_root)
    os.environ["OUTPUT_ROOT"] = str(out_root)
    os.environ["RUN_FULL_COHORT"] = "1" if a.full_cohort else "0"

    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(
        nb, timeout=a.timeout, kernel_name=a.kernel,
        resources={"metadata": {"path": str(nb_path.parent.resolve())}},
    )
    error = None
    t0 = time.time()
    try:
        client.execute()
    except (CellExecutionError, CellTimeoutError) as exc:
        msg = re.sub(r"\x1b\[[0-9;]*m", "", str(exc)).strip().splitlines()
        # Keep the final "SomeError: ..." line plus up to 5 lines after it (the actionable part).
        starts = [k for k, l in enumerate(msg) if re.match(r"^[A-Za-z_.]*(Error|Exception|Interrupt)\b", l)]
        keep = msg[starts[-1]:starts[-1] + 6] if starts else msg[-1:]
        error = {"type": type(exc).__name__, "message": "\n".join(keep)[:800]}
    except Exception as exc:  # kernel failed to start, etc.
        error = {"type": type(exc).__name__, "message": str(exc)[:500]}
    runtime = time.time() - t0

    code_cells = [(i, c) for i, c in enumerate(nb.cells) if c.cell_type == "code"]
    executed = [i for i, c in code_cells if c.get("execution_count") is not None]
    failed_cell = next(
        (i for i, c in code_cells for o in c.get("outputs", []) if o.get("output_type") == "error"), None
    )
    figures = sum(
        1 for _, c in code_cells for o in c.get("outputs", [])
        if o.get("output_type") in ("display_data", "execute_result")
        and any(k in o.get("data", {}) for k in ("image/png", "image/svg+xml", "image/jpeg"))
    )

    out_nb = exec_dir / nb_path.name
    nbformat.write(nb, out_nb)
    record = {
        "notebook": nb_path.name,
        "executed_copy": str(out_nb.relative_to(out_root)),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(terse=True),
            "kernel": a.kernel,
            "packages": versions(),
        },
        # Input identity without the full local path (which may be sensitive).
        "data_root_name": data_root.name,
        "full_cohort": a.full_cohort,
        "code_cells_total": len(code_cells),
        "code_cells_executed": len(executed),
        "first_failed_cell": failed_cell,
        "error": error,
        "figures_rendered": figures,
        "runtime_seconds": round(runtime, 1),
        "succeeded": error is None,
        "reminder": "Mechanical record only. Inspect checkpoints and figures; add the scientific validation record by hand.",
    }
    rec_path = exec_dir / (nb_path.stem + ".validation.json")
    rec_path.write_text(json.dumps(record, indent=2))
    print(json.dumps({k: record[k] for k in ("succeeded", "code_cells_executed", "code_cells_total",
                                             "first_failed_cell", "figures_rendered", "runtime_seconds")}))
    print(f"record: {rec_path}")
    sys.exit(0 if error is None else 1)


if __name__ == "__main__":
    main()
