# Skills

Reusable skills for scientific teaching workflows.

## Available skill

- [`llm-analysis-to-raw-notebooks`](llm-analysis-to-raw-notebooks/SKILL.md) turns a set of LLM-generated neuroimaging or LFP analyses into extensively annotated notebooks organized by processing stage or unifying analysis question. Lessons run from a configurable local data root (or documented external-pipeline outputs when that is the source analysis's starting point), let students inspect data at multiple stages, reproduce every assigned source analysis, compare their own outputs with the LLM results, examine measurement validity and consequential thresholds, and report bounded sensitivity and post-run statistical diagnostics.

The skill includes notebook templates, a lesson checklist, and scripts for static checks and headless execution. It does **not** include research data or finished analyses.

## Use

In an agent that discovers skills from a local skills directory, copy or link the complete `llm-analysis-to-raw-notebooks` folder into that directory. For Codex, the default location is `~/.codex/skills/`. Then ask:

> Use `$llm-analysis-to-raw-notebooks` on the attached folder (or `/path/to/analysis-folder`). Inventory every distinct analysis, find and verify matching local data, and make a notebook per processing stage or question-centered analysis family that runs from the local starting-point data. Explain each transformation and result.

You can attach a folder, point to a local folder, or use the current project workspace. An analysis list and explicit data paths are optional when the available files contain enough information to discover them. The skill reports ambiguous or missing links instead of guessing. See the [skill usage guide](llm-analysis-to-raw-notebooks/README.md) for setup and prompt examples, and the [skill instructions](llm-analysis-to-raw-notebooks/SKILL.md) for the full workflow. The bundled templates are starting points; the author must verify source code and data semantics and execute the lessons locally before claiming reproduction.

## License

MIT. See [LICENSE](LICENSE). This repository retains the license notice from the source `scientific-audit-skills` repository.
