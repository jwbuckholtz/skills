#!/usr/bin/env python3
"""Static checks for teaching notebooks (stdlib only; does not execute anything).

Usage: python check_notebook.py NOTEBOOK.ipynb [MORE.ipynb ...] [--json]

Errors (exit code 1) are contract violations that make a lesson non-portable or
give it side effects. Warnings are heuristics: fix them or have a reason.
"""
import ast
import json
import re
import sys
from pathlib import Path

ABS_PATH = re.compile(r"""["'](/Users/|/home/|/mnt/|/Volumes/|/scratch/|/data/|[A-Za-z]:\\)""")
INSTALL = re.compile(r"^\s*[!%](pip|conda|mamba|uv)\b|\bpip\s+install\b|\bconda\s+install\b", re.M)
NETWORK = re.compile(
    r"urllib\.request|urlretrieve|\brequests\.(get|post)\b|\bhttpx\.|^\s*!\s*(wget|curl)\b"
    r"|datasets\.fetch_\w+|\.data_path\(|openneuro\.download|datalad\s+(get|install)",
    re.M,
)
PLOT = re.compile(r"plt\.(subplots|figure|plot|imshow|scatter|hist)\(|\.plot\(|\.imshow\(|\.scatter\(")
LABELS = re.compile(r"set_xlabel|xlabel\(|set_title|suptitle|set_ylabel|ylabel\(")
SELF_LABELED_PLOT = re.compile(r"plotting\.plot_\w+|plot_topomap|plot_sensors|\.plot_joint|viz\.")
RANDOM_DATA = re.compile(r"np\.random\.(rand|randn|normal|uniform)\b|default_rng\([^)]*\)\.(normal|random|uniform)")
MAX_CODE_RUN = 3
CONCEPT_PARTS = ["Intuition", "Formal definition", "Assumptions", "Sensitivities", "Alternatives", "References"]
PREP_PARTS = ["Decision", "Effect", "Counterfactual"]


def src(cell):
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def check(path):
    errors, warnings = [], []
    try:
        nb = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"cannot parse as JSON: {exc}"], []
    if nb.get("nbformat") != 4 or "cells" not in nb:
        return ["not an nbformat-4 notebook"], []

    cells = nb["cells"]
    code = [(i, src(c)) for i, c in enumerate(cells) if c.get("cell_type") == "code"]
    markdown = "\n".join(src(c) for c in cells if c.get("cell_type") == "markdown").lower()
    all_code = "\n".join(s for _, s in code)

    if "DATA_ROOT" not in all_code:
        errors.append("no DATA_ROOT in any code cell: inputs must come from a configurable local raw-data root")
    if "OUTPUT_ROOT" not in all_code:
        errors.append("no OUTPUT_ROOT in any code cell: generated files need a separate, configurable location")

    run = 0
    for i, c in enumerate(cells):
        s = src(c)
        if c.get("cell_type") != "code":
            run = 0
            continue
        run += 1
        try:
            ast.parse("\n".join(l for l in s.splitlines() if not l.lstrip().startswith(("!", "%"))))
        except SyntaxError as exc:
            errors.append(f"cell {i}: Python syntax error at line {exc.lineno}: {exc.msg}")
        if run == MAX_CODE_RUN + 1:
            warnings.append(f"cell {i}: more than {MAX_CODE_RUN} consecutive code cells without markdown explanation")
        if ABS_PATH.search(s):
            errors.append(f"cell {i}: hard-coded absolute path (breaks on other machines, may leak private paths)")
        if INSTALL.search(s):
            errors.append(f"cell {i}: installs packages; list dependencies in the README instead")
        if NETWORK.search(s):
            errors.append(f"cell {i}: network fetch; lessons read only from local DATA_ROOT")
        if PLOT.search(s) and not LABELS.search(s) and not SELF_LABELED_PLOT.search(s):
            warnings.append(f"cell {i}: plotting call without axis labels or title")
        if c.get("outputs") and any(o.get("output_type") == "error" for o in c["outputs"]):
            warnings.append(f"cell {i}: saved output contains an error traceback")

    concept_cells = prep_cells = 0
    for i, c in enumerate(cells):
        if c.get("cell_type") != "markdown":
            continue
        s = src(c)
        first = s.lstrip().splitlines()[0] if s.strip() else ""
        if re.match(r"#+\s*Concept:", first):
            concept_cells += 1
            missing = [k for k in CONCEPT_PARTS if k.lower() not in s.lower()]
            if missing:
                warnings.append(f"cell {i}: concept cell missing {', '.join(missing)}")
        if re.match(r"#+\s*Preprocessing step:", first):
            prep_cells += 1
            missing = [k for k in PREP_PARTS if k.lower() not in s.lower()]
            if missing:
                warnings.append(f"cell {i}: preprocessing step missing {', '.join(missing)}")
        if "<" in first and ">" in first and re.search(r"<[^>]*>", first):
            warnings.append(f"cell {i}: unfilled template placeholder in heading")
    shared_preprocessing = any(
        src(c).lstrip().lower().startswith("# shared preprocessing")
        for c in cells if c.get("cell_type") == "markdown"
    )
    if not shared_preprocessing:
        if not re.search(r"^#{1,4}\s+Eligibility contract\b", markdown, re.M | re.I):
            warnings.append("no endpoint-specific eligibility contract section: define the executable rule, reasons, support and rationale")
        if "eligibility" not in markdown or "sensitivity" not in markdown:
            warnings.append("eligibility sensitivity not described: show how defensible rules change support and findings")
        if not re.search(r"^#{1,4}\s+Multiplicity contract\b", markdown, re.M | re.I):
            warnings.append("no multiplicity contract section: define the full tested family and method, or state no inference")
    if concept_cells == 0:
        warnings.append("no '### Concept:' cells: concepts, measures, and methods need in-depth explanation before use")

    if RANDOM_DATA.search(all_code) and "synthetic" not in markdown:
        warnings.append("random data generation found but no markdown says 'synthetic': label demos so they are not read as observed results")
    if not code:
        errors.append("notebook has no code cells")
    return errors, warnings


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__)
        return 2
    report, failed = {}, False
    for p in paths:
        e, w = check(p)
        report[p] = {"errors": e, "warnings": w}
        failed |= bool(e)
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        for p, r in report.items():
            status = "FAIL" if r["errors"] else "ok"
            print(f"{status}  {p}")
            for e in r["errors"]:
                print(f"  ERROR    {e}")
            for w in r["warnings"]:
                print(f"  warning  {w}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
