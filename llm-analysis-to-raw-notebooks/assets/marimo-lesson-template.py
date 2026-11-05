"""Native marimo analysis-family lesson TEMPLATE. Replace placeholders before scientific use."""
import marimo

__generated_with = "0.0.0"
app = marimo.App()

@app.cell
def _():
    import os
    from pathlib import Path
    import marimo as mo
    import numpy as np
    return os, Path, mo, np

@app.cell
def _(mo):
    mo.md("""
# Analysis family: <scientific question>

**Learning objectives:** reproduce the source analysis from verified starting-point data;
explain the estimand, measurement validity, assumptions, sensitivity and inference.

**Source:** <analysis IDs, revision, output artifacts and comparison tolerances>.
**Starting point:** <raw data or versioned external pipeline outputs>.
**Do not treat this template as evidence of a completed reproduction.**
""")
    return

@app.cell
def _(Path, os):
    DATA_ROOT = Path(os.environ.get("DATA_ROOT", "./data")).expanduser()
    OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "./outputs")).expanduser()
    RUN_FULL_COHORT = os.environ.get("RUN_FULL_COHORT", "0") == "1"
    # Opening the notebook must not download data, install packages or launch a full run.
    return DATA_ROOT, OUTPUT_ROOT, RUN_FULL_COHORT

@app.cell
def _(mo):
    mo.md("""
### Concept: <method>
**Intuition:** <...>
**Formal definition:** <equation, symbols and units>
**Assumptions:** <...>
**Sensitivities:** <...>
**Alternatives:** <...>
**References:** <verified citations>

### Student checkpoint: predict → inspect → explain
Predict an observable result *before* executing the next analysis step.
After inspecting the real-data diagnostic, explain agreement or disagreement.

### Eligibility contract
<source rule, per-unit reasons and support>

### Multiplicity contract
<full test family, target error rate, correction method or no inference>
""")
    return

@app.cell
def _(DATA_ROOT, mo):
    # Replace with read-only verification of the exact raw/external-pipeline input.
    # Never substitute synthetic data for the source reproduction.
    mo.md(f"Configured DATA_ROOT: `{DATA_ROOT.name}`. **Input verification pending.**")
    return

@app.cell
def _(mo):
    mo.md("""
### Reproduce source analysis
Implement the **source specification first** and compute intermediate checkpoints.
Expensive full-cohort jobs must be explicitly gated and never run on notebook open.

### Bounded sensitivity analysis
Implement all prespecified scenarios as deterministic code. Optionally **offer**
a marimo selector for inspecting them, but never require UI interaction to run them.
Keep every scenario and unfavorable outcome visible.

### Source-versus-student comparison
Compare version/cohort, source value, computed value, difference, tolerance and
match/mismatch/unavailable status. Never invent a source number.

### Independent assessment
Recreate one transformation and defend its estimand, assumptions, uncertainty,
diagnostics and interpretation. Provide a rubric and delayed worked explanation.
""")
    return

if __name__ == "__main__":
    app.run()
