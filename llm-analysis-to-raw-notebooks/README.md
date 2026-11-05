# Raw-data teaching notebooks

Use this skill to turn a set of neuroimaging or LFP analyses into notebooks organized by processing stage or unifying analysis question. It inventories the analyses, links each one to verified local inputs, and teaches the operations from the source analysis's starting point through figures and inference. The skill is an instruction set for a coding agent; the scripts in this folder check and execute notebooks after the agent creates them.

## Install and invoke

Copy or link the entire `llm-analysis-to-raw-notebooks` folder into your agent's skills directory. For Codex, that is usually `~/.codex/skills/`. Then invoke **`$llm-analysis-to-raw-notebooks`** in a chat with access to the analysis materials. You can also mention the skill by name in a request.

You may attach a folder, provide a local path, or work in an open project. A hand-written list of analyses and explicit data paths are optional when the available files identify them. The agent should first inventory the material, map distinct analyses to source code and outputs, and verify any proposed data links. It should ask about unresolved ambiguity rather than guess. Attached analysis code and reports do not themselves supply raw data; if the necessary local inputs are unavailable, the affected analysis is marked as blocked for raw-data reproduction.

The notebook output uses a configurable `DATA_ROOT` and separate `OUTPUT_ROOT`. Paths discovered on the author's machine are for validation, not hard-coded into published lessons. The original analyses and raw files remain intact.

## How notebooks are grouped

The default unit is a processing stage or a question-centered analysis family, not an individual script, contrast, or output table. For example, a pipeline could have `00_preprocessing.ipynb`, `01_first_level_maps.ipynb`, and `02_reward_representation.ipynb`; the last notebook may contain several related contrasts and sensitivity analyses. Every member analysis still gets its own eligibility and multiplicity contract, outputs, and interpretation. You can request finer notebook boundaries explicitly.

Every example below inherits the minimum deliverable: the student runs the assigned source stage or every member analysis on local inputs, inspects data at multiple stages, and compares their results with the recorded LLM output using named criteria. If a reference output is absent, the lesson reports that comparison as incomplete.

## Prompt examples

Use the example that matches your situation. Replace paths and analysis names only where you have them.

### Uploaded folder with many analyses

> Use `$llm-analysis-to-raw-notebooks` on the folder I attached. Inventory all distinct analyses, including reruns and sensitivity branches, and show how each maps to producer code, inputs, and saved outputs. Find matching local data where accessible, then make one notebook per processing stage or question-centered analysis family, with each member analysis documented inside its family notebook. Document unresolved links and excluded candidates.

### Current project, with automatic discovery

> Use `$llm-analysis-to-raw-notebooks` for this project. Find the analyses and their local starting-point data from the project code and manifests, verify each match against the actual files, and build stage notebooks and question-centered analysis-family notebooks. Explain every transformation and visualize each meaningful output.

### Explicit code and data locations

> Use `$llm-analysis-to-raw-notebooks` on `/path/to/analysis-code` with local raw data at `/path/to/data`. Group A and B if they answer one question; keep C separate if it answers another. Compare computed outputs with the recorded results and report any mismatch or step that cannot be verified.

### Folder contains analyses, but data may be missing

> Use `$llm-analysis-to-raw-notebooks` on the attached analysis folder. First inventory every analysis and identify the exact raw or external-pipeline inputs it needs. Build and validate lessons for analyses whose inputs are available locally. For the rest, give me a precise missing-input list and do not substitute saved feature tables as raw data.

### Source starts from an external preprocessing pipeline

> Use `$llm-analysis-to-raw-notebooks` for these fMRI analyses. The source starts from local fMRIPrep outputs at `/path/to/derivatives`. Teach the upstream pipeline steps from its version, configuration, logs, and reports, mark that boundary in every lesson, and execute the source analysis from those outputs onward.

### Focused teaching scope and format

> Use `$llm-analysis-to-raw-notebooks` for the F01 parent analyses only. Make a separate `.ipynb` for preprocessing and each question-centered F01 family, with matching marimo `.py` companions. Keep explicit sections for each member analysis. Assume a student knows general neuroimaging but is new to LFPs and multivariate methods. Keep the source results and any eligibility or multiplicity sensitivities visibly separate.

### Measurement, eligibility, and multiplicity choices

> Use `$llm-analysis-to-raw-notebooks` for this analysis set. For each endpoint, show whether the dataset can measure the target, implement a defensible trial-eligibility contract, and compare a small set of justified eligibility rules. Define the full tested family for each inferential claim and let students recalculate predeclared correction scenarios on the fly. Show support, estimates, uncertainty, and unfavorable results for every scenario.

## What to expect

A completed lesson set should include an index with run order and provenance, a notebook per processing stage or question-centered analysis family, and a coverage ledger that distinguishes completed reproduction from a bounded test or missing inputs. Every notebook lets the student run its assigned source stage or all member analyses themselves and compare their output with the recorded LLM result. Each family notebook teaches the biological question, measurement, source operations, inclusion rules, model, inference, sensitivity checks, and interpretation limits. It should give the student hands-on checkpoints at multiple data stages, worked explanations, and a source-versus-student comparison for every assigned output. Missing source results remain an explicit incomplete deliverable.

A notebook that merely loads a saved result is not a raw-data reproduction. A small real-data run checks the pipeline but does not certify the full cohort. Missing input or ambiguous event meaning should be reported, not filled in with a synthetic example.

## Formats and learning controls

Default output is **native marimo** (`.py`); request Jupyter (`.ipynb`) or both, or set `NOTEBOOK_FORMAT=marimo|jupyter|both`. Both formats are audited and executed separately against the same source analysis and input cohort.

Interactive controls are offered when helpful, never required: every lesson retains deterministic source reproduction, source comparison and predefined sensitivity scenarios without widgets. Predict–inspect–explain checkpoints and an independent exercise with answer criteria test student understanding.

```bash
python scripts/check_marimo.py notebooks/02_question.py
python scripts/run_marimo.py notebooks/02_question.py --data-root "$DATA_ROOT" --output-root "$OUTPUT_ROOT"
marimo edit notebooks/02_question.py  # optional manual UI review
```

The marimo runtime test exports static HTML and a validation JSON; it cannot certify interactive widget behavior or scientific validity by itself. Install required dependencies separately in advance; lessons do not download data or packages.

## Running the generated notebooks

Follow the generated lesson set's own README for its exact packages, data layout, run order, and resource needs. Set `DATA_ROOT` to your local input copy and `OUTPUT_ROOT` to a separate writable directory. The bundled `scripts/check_notebook.py` performs static checks; `scripts/run_notebook.py` can execute a generated `.ipynb` and save an executed copy plus a validation record when `nbformat`, `nbclient`, and a Jupyter kernel are already available. Neither script installs packages or downloads data. Full-cohort work is a deliberate action, not a side effect of opening a notebook.

For the detailed authoring requirements, read [SKILL.md](SKILL.md) and the [lesson contract](references/lesson-contract.md).
