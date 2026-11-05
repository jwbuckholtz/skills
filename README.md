# Skills

Reusable skills for scientific teaching workflows.

## Available skill

- [`llm-analysis-to-raw-notebooks`](llm-analysis-to-raw-notebooks/SKILL.md) turns a set of LLM-generated neuroimaging or LFP analyses into separate, extensively annotated teaching notebooks. Lessons run from a configurable local data root (or documented external-pipeline outputs when that is the source analysis's starting point), show the effect of each transformation, examine measurement validity and consequential thresholds, and report bounded sensitivity and post-run statistical diagnostics.

The skill includes notebook templates, a lesson checklist, and scripts for static checks and headless execution. It does **not** include research data or finished analyses.

## Use

In an agent that discovers skills from a local skills directory, copy or link the complete `llm-analysis-to-raw-notebooks` folder into that directory. For Codex, the default location is `~/.codex/skills/`. Then ask:

> Use `$llm-analysis-to-raw-notebooks` to turn the analyses in `/path/to/analysis/repository` into teaching notebooks. My local data are under `/path/to/data`. Make a separate notebook per analysis and explain each transformation and result.

Read the [skill instructions](llm-analysis-to-raw-notebooks/SKILL.md) for the full workflow and input requirements. The bundled templates are starting points; the author must verify source code and data semantics and execute the lessons locally before claiming reproduction.

## License

MIT. See [LICENSE](LICENSE). This repository retains the license notice from the source `scientific-audit-skills` repository.
