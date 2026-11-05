# <Lesson set title>

Teaching notebooks that reproduce <N> analyses from <source repository/report> starting from local raw data.

## Analysis folder intake

- Supplied folder or archive: <anonymized location and content fingerprint>
- Inventory: <scripts, notebooks, specifications, manifests, reports, outputs and data references>
- Analysis ledger: <link to coverage manifest; name excluded, duplicate, and unresolved candidates>
- Source-to-data linking: <evidence used to match each analysis to its local inputs; name ambiguities>

## Run order

| # | Notebook | Analysis ID | Depends on | Reproduction level reached |
|---|---|---|---|---|
| 0 | `00_shared_preprocessing.ipynb` | — | — | <mechanics / plumbing / full> |
| 1 | `01_<analysis>.ipynb` | <id> | 0 | |

## Starting point

| Notebook | Starts from | Upstream steps |
|---|---|---|
| `01_<analysis>.ipynb` | <raw acquisition data \| <pipeline> <version> outputs> | <executed here \| explained from pipeline logs/reports, not re-executed> |

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
python scripts/run_notebook.py notebooks/01_<analysis>.ipynb --data-root "$DATA_ROOT" --output-root "$OUTPUT_ROOT"
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

## Reproduction boundaries

- <what was reproduced exactly, within tolerance, not compared, or unresolved>
- Synthetic fixtures (if any) validate mechanics only; bounded real-data runs validate plumbing only.
