# <Lesson set title>

Teaching notebooks organized by processing stage or unifying question that reproduce <N> analyses from <source repository/report> starting from local raw data.

## Analysis folder intake

- Supplied folder or archive: <anonymized location and content fingerprint>
- Inventory: <scripts, notebooks, specifications, manifests, reports, outputs and data references>
- Analysis ledger: <link to coverage manifest; name excluded, duplicate, and unresolved candidates>
- Source-to-data linking: <evidence used to match each analysis to its local inputs; name ambiguities>

## Output format, assessment and validation

- Primary backend: <marimo|jupyter|both>; canonical source if paired: <path>
- Optional interactivity offered: <controls or none>; deterministic noninteractive path: <details>
- Student assessment: <prediction checkpoints, answer criteria and independent exercise>
- Validation for each backend: <syntax/DAG/headless/scientific/UI statuses>

## Run order

| # | Notebook | Stage or unifying question | Member analysis IDs | Depends on | Reproduction level reached |
|---|---|---|---|---|---|
| 0 | `00_preprocessing.ipynb` | Preprocessing | — | — | <mechanics / plumbing / full> |
| 1 | `01_first_level_maps.ipynb` | First-level map creation | <ids> | 0 | <status> |
| 2 | `02_<question_family>.ipynb` | <unifying question> | <ids> | 1 | <status> |

Map every source analysis to a member section in its stage or family notebook; justify any split or grouping that is not obvious.

## Starting point

| Notebook | Starts from | Upstream steps |
|---|---|---|
| `02_<question_family>.ipynb` | <raw acquisition data \| <pipeline> <version> outputs> | <executed here \| explained from pipeline logs/reports, not re-executed> |

## Local data setup

- Expected layout under `DATA_ROOT`: <tree or pattern>
- Required metadata files: <...>
- Set before launching Jupyter: `export DATA_ROOT=/path/to/raw OUTPUT_ROOT=/path/to/outputs`
- Nothing is downloaded. Missing inputs stop the discovery cell with the exact path.

## Dependencies

Must already be installed (the notebooks do not install anything): <python version, packages with versions>

## Commands

```bash
python scripts/check_notebook.py notebooks/*.ipynb
python scripts/run_notebook.py notebooks/02_<question_family>.ipynb --data-root "$DATA_ROOT" --output-root "$OUTPUT_ROOT"
# full cohort (deliberate):
RUN_FULL_COHORT=1 python scripts/run_notebook.py ... --timeout 7200
```

## Runtime and storage

| Notebook | Bounded run | Full cohort | Peak memory | Disk written |
|---|---|---|---|---|

## Provenance

Source: <repo/path> @ <commit>. Per-analysis source paths, parameters and seeds are in each notebook's source map and in `coverage_manifest.json`.

## Eligibility contracts and sensitivity

| Analysis | Source eligibility rule | Endpoint-specific rationale | Units retained/lost | Alternative rules tested | Finding change |
|---|---|---|---|---|---|
| <id> | <source/code> | <measurement and estimator support> | <by hierarchy and reason> | <bounded alternatives> | <estimate, uncertainty, inference> |

Each notebook contains the executable rule, row-level reason ledger, and figures for support and finding changes. A rule for one endpoint does not define whole-session usability.

## Multiplicity contracts and sensitivity

| Analysis/claim | Complete tested set | Source family and method | Defensible scenarios | Effect of scenarios |
|---|---|---|---|---|
| <id/claim> | <tests and dependence> | <family size, method, target error rate or no inference> | <predeclared alternatives> | <adjusted values, uncertainty and interpretation> |

Optional notebook controls recompute named scenarios from the full fixed test ledger; deterministic code always evaluates every prespecified scenario. The source correction and all tested results remain visible.

## Student-run outputs and source comparison

| Notebook | Source stage or member analysis | Source artifact/version and cohort | Student result and cohort | Difference/criterion | Status |
|---|---|---|---|---|---|
| <notebook> | <stage or analysis ID> | <recorded LLM output> | <local output> | <tolerance or paired figure criterion> | <match/mismatch/unavailable> |

Each notebook includes hands-on checkpoints at several data stages, worked answer criteria, and a comparison for every assigned source output. An unavailable reference or a bounded-only run is explicitly incomplete for full reproduction.

## Reproduction boundaries

- <what was reproduced exactly, within tolerance, not compared, or unresolved>
- Synthetic fixtures (if any) validate mechanics only; bounded real-data runs validate plumbing only.

## Marimo commands (if selected)

```bash
python scripts/check_marimo.py notebooks/*.py
python scripts/run_marimo.py notebooks/02_question.py --data-root "$DATA_ROOT" --output-root "$OUTPUT_ROOT"
marimo edit notebooks/02_question.py
```

Headless static HTML export does not test reactive controls. Validate optional interactions separately, and never claim full-cohort reproduction from a bounded run.
