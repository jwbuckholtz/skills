"""Native marimo processing-stage template. Replace placeholders with verified source operations."""
import marimo

__generated_with = "0.0.0"
app = marimo.App()

@app.cell
def _():
    import os
    from pathlib import Path
    import marimo as mo
    return os, Path, mo

@app.cell
def _(mo):
    mo.md("""
# Processing stage: <stage name>
**Starting data:** <verified raw acquisitions or external pipeline outputs>
**Source revision:** <version>
**Goal:** independently reproduce the specified source-stage artifact.

### Concept: <stage transformation>
**Intuition:** <...>
**Formal definition:** <...>
**Assumptions:** <...>
**Sensitivities:** <...>
**Alternatives:** <...>
**References:** <...>

### Student checkpoint: predict → inspect → explain
Predict the effect on dimensions, units, retained observations, and artifacts.
""")
    return

@app.cell
def _(Path, os):
    DATA_ROOT = Path(os.environ.get("DATA_ROOT", "./data"))
    OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "./outputs"))
    RUN_FULL_COHORT = os.environ.get("RUN_FULL_COHORT", "0") == "1"
    return DATA_ROOT, OUTPUT_ROOT, RUN_FULL_COHORT

@app.cell
def _(mo):
    mo.md("""
### Source comparison
Run the actual stage from the declared starting point. Compare the computed
artifact with the source artifact using recorded version, cohort and tolerances.

### Assessment
Reproduce a meaningful stage transformation independently and interpret failures.
**Status:** incomplete until verified against real local inputs.
""")
    return

if __name__ == "__main__":
    app.run()
