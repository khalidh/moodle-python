---
name: moodle-python
description: Generate, validate, evaluate, and publish French Moodle courses with OpenAI using the bundled Moodle Python pipeline, course schema, pedagogical prompts, quality checklist, and operational workflows. Use this skill when asked to create or adapt Moodle learning content, run the Moodle generation pipeline, inspect the context engineering setup, validate course JSON/XML outputs, or explain this Moodle training project.
---

# Moodle Python

## What This Skill Does

Use this skill to work on a French context-engineering pipeline that turns pedagogical requirements into Moodle-ready course content:

1. Load the system prompt and domain prompt from `assets/prompts/`.
2. Generate structured course JSON with OpenAI.
3. Validate and normalize the generated JSON.
4. Render Moodle book HTML chapters and Moodle XML quizzes.
5. Optionally publish to Moodle or generate the archived Google Docs variant.
6. Evaluate the output with the checklist in `references/evals/quality_checklist.md`.
7. Run deterministic harness scenarios before external end-to-end checks.

## Quick Workflow

For local validation without external API calls:

```bash
venv/bin/python -m pytest
venv/bin/python -m json.tool assets/examples/formation_minimale.json
venv/bin/python scripts/run_harness.py
```

For Moodle generation and publication, ensure `.env` contains OpenAI and Moodle credentials, then run:

```bash
python scripts/generation_moodle.py
```

For the Google Docs variant, ensure Google credentials are configured, then run:

```bash
python scripts/generation_google_docs.py
```

## Resource Map

- `scripts/`: executable pipelines.
- `src/moodle_python/`: reusable Python services and utilities.
- `assets/prompts/`: prompts, schema contract, and Moodle HTML template used by the pipeline.
- `assets/examples/`: short stable inputs and sample course JSON for tests and workshops.
- `references/workflows/`: step-by-step operating procedures.
- `references/evals/quality_checklist.md`: quality review checklist for generated Moodle courses.
- `harness/`: deterministic validation scenarios and expected checks for agent/CI use.
- `references/project/docs/`: architecture notes, context map, workshops, decisions, and backlog.
- `output/`: local generated artifacts; treat as disposable runtime output.

## When Editing

- Keep runtime resources in `assets/`, not in `references/`.
- Keep detailed explanatory material in `references/`, not in `SKILL.md`.
- Update `src/moodle_python/config.py`, `.env.example`, tests, and workflow docs whenever a default path changes.
- Prefer adding tests around prompt loading, JSON validation, or Moodle rendering when changing the pipeline.
- Add or update `harness/scenarios/*.yaml` when changing contracts, fixtures, prompt rendering, or Moodle export behavior.

## References To Load As Needed

- Architecture overview: `references/project/docs/architecture.md`
- Context layers: `references/project/docs/context-engineering/context-map.md`
- Output contract: `assets/prompts/contracts/course_schema.md`
- Local validation procedure: `references/workflows/validation-locale.md`
- Moodle generation procedure: `references/workflows/generation-moodle.md`
- Harness guide: `harness/README.md`
