---
name: llm-analysis-to-raw-notebooks
description: Turn a set of LLM-generated scientific analyses into separate, heavily annotated teaching notebooks that reproduce each analysis from local raw data. Use when the user provides analysis code, reports, or a repository and asks for executable lessons, across neuroimaging and LFP workflows, including MRI, fMRI, diffusion, PET, EEG, MEG, and intracranial recordings.
---

# Analysis-to-notebook teaching skill

Build Jupyter (`.ipynb`) lessons that a student can run locally from raw data, inspect at every transformation, and compare with the source analysis. These are teaching materials first: the verification machinery exists so that what the student learns is true, not as a substitute for teaching.

Unless the user specifies otherwise, write for a PhD student who is comfortable with statistics, linear algebra, and programming but may be new to this modality, this measure, or this analysis family. Explain every concept, measure, preprocessing step, and analysis in depth, including ones that seem standard: a PhD student needs to be able to defend each choice in a lab meeting or a review, which requires knowing why it was made and what would change without it, not just what it is called. If the user names a different audience, adjust depth and vocabulary but keep the same coverage.

Treat generated prose and code as claims to verify, not as an authority. LLM-written analyses often describe steps their code never performs, or mislabel what a variable holds; a lesson that inherits those errors teaches them. Preserve the biological question, estimand, sampling unit, and limits of each analysis, because a lesson that quietly changes any of these is teaching a different analysis.

This is an authoring workflow for teaching materials. It works on any supplied analysis set; it does not need a published paper or a particular repository layout. If the material arrives from a workflow with access restrictions (for example a blinded review where some outputs must stay unseen), follow those restrictions and copy only the inputs you are permitted to use into the teaching workspace — breaking a blind cannot be undone by the lesson.

## Bundled resources

- `references/lesson-contract.md` — the checklist for what each lesson must show and how to record validation. Read it before writing the first notebook.
- `assets/lesson-template.ipynb` — the cell skeleton every analysis lesson starts from (question, config, discovery, source map, concept cells, preprocessing and analysis steps, comparison, limits, validation record). Copy it per analysis and fill it in; delete sections that do not apply rather than leaving them empty.
- `assets/preprocessing-template.ipynb` — the skeleton for a shared preprocessing lesson, including the pipeline-boundary declaration and per-step concept/decision/effect cells.
- `assets/README-template.md` — the index/README skeleton for the delivered lesson set.
- `assets/coverage-manifest.example.json` — the machine-readable coverage manifest format.
- `scripts/check_notebook.py` — static checks (stdlib only): configurable `DATA_ROOT`/`OUTPUT_ROOT`, no hard-coded absolute paths, no package installs or network fetches, every code cell explained by adjacent markdown, plotting cells that set axis labels, and concept cells that cover the required elements. It cannot judge whether an explanation is good — read the notebook as the student would. Run it on every notebook before executing.
- `scripts/run_notebook.py` — executes a notebook headlessly with `DATA_ROOT`/`OUTPUT_ROOT` set and writes a JSON validation record (environment, cells executed, errors, figures rendered, runtime). Requires `nbformat` and `nbclient` already present; it reports what is missing rather than installing anything.

## Scope and source audit

1. Inventory the supplied analysis set before writing notebooks. Map each distinct analysis to its question, producer code, raw inputs, preprocessing dependencies, saved outputs, version, and status. Distinguish parent analyses, sensitivities, extensions, and duplicate versions. Write one notebook per analysis, plus a separate shared preprocessing lesson when several analyses share an upstream path (so students do not relearn — or see inconsistent versions of — the same steps). Present a related analysis as related: calling a sensitivity analysis an independent replication overstates the evidence.
2. Trace each computational path back to local raw files and the metadata needed to interpret them. Inspect the actual objects and source code. Establish the modality-appropriate acquisition metadata, physical units, coordinate or time bases, spatial or sensor layout, events/labels, masks, and participant/session identifiers. Document missing or ambiguous mappings. Derive event semantics, anatomical meaning, and data quality from metadata and inspection of the data itself: filenames and array shapes are routinely wrong or ambiguous (a `trial_type` column coded 1/2, an array whose axes could be channels × time or time × channels), and a wrong guess silently changes the result.
3. Define the lesson's starting point. By default it is the raw acquisition data. The one exception: when the source analysis itself starts from the outputs of an established external preprocessing pipeline (fMRIPrep, QSIPrep, FreeSurfer, MNE-BIDS-Pipeline, Kilosort, and similar), the lesson starts from those pipeline outputs, because that is where the source's own computation begins and rerunning the pipeline would reproduce a different program, not the analysis. In that case:
   - Read the pipeline's version, configuration, logs, and reports (HTML reports, `dataset_description.json`, boilerplate/citation text, confound files) and teach each step the pipeline ran, in the same depth as steps the lesson runs itself, with the pipeline's own QC figures or plots of its outputs.
   - State the boundary visibly at the top of the notebook and in the README: "reproduced from <pipeline> <version> outputs; upstream steps explained from its logs and reports, not re-executed."
   - Mark any pipeline step you cannot confirm from those records as unresolved.
   - This exception covers external pipelines only. The source analysis's own intermediate files (its feature tables, cached epochs, saved model inputs) are still comparison targets, never starting points.
4. If the inputs at the lesson's starting point (raw data, or the external pipeline outputs when step 3 applies) are not available locally, stop for that analysis and report exactly what is missing (files, metadata, where the source code expects them). Do not build a proxy path from other derivatives, caches, or synthetic data: the purpose of these lessons is the chain from the starting point to the result, and a lesson that substitutes something else would look complete while teaching an unverified path.
5. Keep source analysis and teaching implementation linked. Record exact source paths, version/commit or hash when available, parameter values, random seeds, and any deliberate simplification. If a claimed operation cannot be verified in code or raw data, label it unresolved instead of substituting a convenient proxy — the label tells the student where the source claim is weak; a proxy hides it.

## Measurement and analysis fit

Before reproducing a model, ask what physical or behavioral quantity the available data actually measure and whether its resolution, coverage, timing, calibration, reliability, and sampling support the proposed estimand. Trace the path from acquisition to construct: units and coordinate systems, event/label validity, spatial or sensor localization, missingness and censoring, signal-to-noise and artifacts, and the population represented. Show a real-data diagnostic for the material risks. Distinguish a technically computable feature from a valid measure of the intended construct. If the dataset cannot identify the target, state the narrower estimand it supports or mark the analysis measurement-limited; do not quietly change the scientific question.

## Local raw-data execution

- Read inputs from a user-configurable `DATA_ROOT` (environment variable with one clearly marked configuration cell, as in the template) pointing to a local copy of the starting-point data (raw, or external pipeline outputs per step 3 above), and write everything generated under a separate `OUTPUT_ROOT`. Keep raw files and historical analysis outputs untouched, because they are the reference the lesson is compared against. Use no developer-specific absolute paths in runnable code; they break the notebook on every other machine and can leak private directory structure.
- Start with a read-only discovery cell that lists expected files and checks schemas/metadata, raising an actionable error for absent or incompatible data. Keep notebook import/open free of side effects — no downloads, package installs, or large computations — so that opening a lesson never changes the student's environment, consumes their bandwidth, or starts an hour-long job they did not ask for.
- Run the real upstream operations from the starting point onward: raw read; modality-appropriate calibration, synchronization, spatial registration or event alignment; quality control; preprocessing; unit construction; feature or image-measure extraction; estimator fitting; validation/inference; and figures, as applicable. A frozen table or feature cache may serve as a comparison target, but not as the computational input for a claimed raw-data reproduction — starting from the cache would skip exactly the steps the lesson exists to teach and verify.
- Preserve the source analysis's eligibility, split, weighting, unit of inference, multiple-comparison family, and failure behavior. Explain any deviation and its effect on the estimand. Keep optional model searches and new inference out of anything labeled a reproduction; extra analyses change the error rates and make the comparison with the source meaningless. Put teaching variations in a clearly separate, labeled section after the reproduction.
- Bound memory/runtime with an explicit subset selection, lazy or chunked reads when needed, progress messages, and estimated resource needs. A small real-data smoke run demonstrates plumbing but cannot certify full-cohort results. Make full-cohort execution a deliberate, visible action (a flag in the config cell) so a student never triggers it by accident.

## Teaching design

For each notebook, explain the question and possible positive, negative, and measurement-limited outcomes before inference, so the student commits to what each result would mean before seeing it.

### Concept cells

Before the code that first uses a concept, measure, preprocessing step, or analysis method, write a concept cell. A one-line definition is not an explanation; a student who only knows the name cannot judge whether the method was appropriate. Each concept cell covers, as applicable:

1. **Intuition** — what the method does to the data and what problem it solves, in plain language.
2. **Formal definition** — the equation or algorithm, with every symbol defined and its units/dimensions stated.
3. **Assumptions** — what must be true of the data for the result to mean what it claims (stationarity, independence, linearity, Gaussian noise, correct registration, …).
4. **Sensitivities and failure modes** — what inflates, biases, or breaks it, and what that would look like in the figures.
5. **Alternatives and the choice** — the main alternative approaches, how they differ, and why the source analysis used this one (or that the source gives no reason).
6. **Worked toy example** — a small, clearly labeled synthetic example the student can compute by hand or reason through, when it clarifies the mechanism. Keep it visibly separate from the real-data path.
7. **Primary references** — the method's original or canonical paper(s) and any key methodological critique. Cite only references you can verify; if unsure, name the topic to look up instead of inventing a citation.

Concepts reused across notebooks can be taught fully once (for example in the shared preprocessing lesson) and cross-referenced afterward, but each notebook must state the assumptions that matter for its own analysis.

### Preprocessing steps

Teach preprocessing with the same depth as the analysis, because preprocessing choices often move results more than the estimator does. For each step (whether the lesson runs it or an external pipeline ran it), give a concept cell plus:

- **The decision**: the exact parameter values used (filter type, order, and cutoffs; reference scheme; ICA algorithm and component-rejection criteria; motion/scrubbing thresholds; smoothing kernel; registration target and interpolation; confound set; bad-channel/trial criteria) and where each value came from (source code, pipeline config, default).
- **The effect**: a before/after figure or numerical comparison on real data showing what the step changed, and what was lost (channels, trials, volumes, participants).
- **The counterfactual**: what plausibly reasonable alternative settings would do and which downstream results they would most likely affect. Explain this, and run a bounded, separately labeled sensitivity when a consequential choice is uncertain. Keep it outside the reproduction result.

### Thresholds, choices, and sensitivity

Inventory user-specifiable and implementation choices that can affect eligibility, the measurement, or the estimate: for example filter family/order/cutoffs, artifact and motion thresholds, referencing, smoothing, epoch/window length, masks, feature definitions, model hyperparameters, and statistical cutoffs. For each, show the source value, units, where it came from, plausible range or alternatives grounded in the data and method, and which outputs it can change. A threshold is a measurement or design decision, not merely a code constant. Visualize values near the threshold and the resulting support/attrition before interpreting downstream estimates.

Reproduce the source specification first. Then, where a consequential choice is uncertain and a bounded alternative addresses a concrete measurement or design risk, run a separately labeled sensitivity analysis on the same local data. Define the alternatives and stopping rule before viewing their results; preserve all attempted settings, denominators, effect sizes, uncertainty and relevant figures. Explain whether the alternative changes the measurement or estimand, and compare at the appropriate participant/animal/session level. Do not run an open-ended sweep, optimize for a desired result, or relabel the sensitivity as independent replication. If a sensitivity cannot be run, explain the dependency or resource limit and the impact on interpretation.

### Transformations and figures

At every substantive operation, state input/output shape, dimensions, units, sampling level, purpose, exact transformation, and a checkable intermediate result. Annotate functions so students can see what changes in the data and why. Explain spatial/temporal alignment, leakage, cross-validation, nulls, and multiplicity where they arise.

Every analysis output that admits a meaningful visualization gets one. Include figures for raw measurements or images, spatial/sensor layout, QC and attrition, alignment, preprocessing effects, feature or image-measure distributions, fitted/predicted structure, participant/session variation, uncertainty, nulls, and unfavorable outcomes as applicable. Plot intermediate arrays when they clarify the operation. Give every plot axes or anatomical coordinates, units, denominator, and interpretation limits. For an output without a useful plot, state why a table or text is more faithful. Label any synthetic demonstration as synthetic, everywhere it appears, so it is never mistaken for observed-data results.

## Post-run statistical review

After producing the results, inspect the realized design and model behavior, not only whether code completed. Reconcile sample counts and exclusions; check dependence and the actual unit of inference, split leakage, class/condition support, convergence and numerical stability, calibration of null or permutation procedures, interval coverage assumptions, multiplicity families, and influential participants/sessions or outliers as relevant. Use diagnostics and limited follow-up checks to identify statistical issues exposed by the data. Report the issue, evidence, affected analyses, possible direction of bias, and whether a corrected same-estimator rerun or a changed statistical model would be required. Keep the original result and the diagnostic visible. Do not replace the source analysis or interpret a post-hoc repair as preplanned evidence without labeling it.

## Verification and deliverables

Use `references/lesson-contract.md` as the output and validation checklist. For each notebook:

1. Run `python scripts/check_notebook.py <notebook.ipynb>` and fix every error (warnings need a reason if left).
2. Execute a bounded local raw-data path with `python scripts/run_notebook.py <notebook.ipynb> --data-root ... --output-root ...`, then inspect numerical checkpoints and plots yourself — a notebook that runs without error can still compute the wrong thing.
3. Run the full requested scope when the data and resources support it.
4. Compare computed outputs with the source analysis using named tolerances and explain differences.

Clearly separate source inspection, code execution, empirical reproduction, and scientific interpretation in what you report. Report failed or missing inference as failed or missing; a filled-in number that was never computed is worse than a gap, because the student will trust it.

Deliver an index/README (from `assets/README-template.md`) with run order, local data setup, dependencies, provenance, per-analysis coverage, expected outputs, commands, runtime/storage expectations, and reproduction boundaries. Include a coverage manifest (format in `assets/coverage-manifest.example.json`) when the set has more than a few analyses. Keep original analyses and outputs intact. Commit or publish only when the user or repository workflow authorizes it.
