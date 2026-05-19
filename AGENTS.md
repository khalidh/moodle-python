# Agent Instructions

This repository is both an Open Skill and a Python software project for generating Moodle course content.

## Project Shape

- `SKILL.md` is the Open Skill entry point.
- `agents/openai.yaml` contains Open Skill interface metadata.
- `scripts/` contains executable pipelines.
- `src/moodle_python/` contains Python package code.
- `assets/` contains runtime resources used by scripts and tests.
- `references/` contains documentation, workflows, evaluations, and project notes.
- `harness/` contains deterministic scenarios for agent and CI validation.
- `tests/` contains local regression tests.
- `output/` contains generated artifacts and should be treated as disposable.

## Working Rules

- Keep reusable Python code in `src/moodle_python/`.
- Keep operational scripts in `scripts/`.
- Keep prompts, templates, schemas, and examples in `assets/`.
- Keep explanatory or procedural documentation in `references/`.
- Do not move secrets or generated outputs into the skill resources.
- Do not commit or expose `.env`, `secrets/`, Moodle tokens, OpenAI keys, Google credentials, or generated `output/` files.
- If a default path changes, update `src/moodle_python/config.py`, `.env.example`, tests, workflows, and relevant references together.
- Prefer focused edits over broad refactors.

## Validation

Run the local checks before considering a change complete:

```bash
venv/bin/python -m pytest
venv/bin/python -m json.tool assets/examples/formation_minimale.json
venv/bin/python -m py_compile scripts/generation_moodle.py scripts/generation_google_docs.py src/moodle_python/config.py src/moodle_python/services/openai_service.py src/moodle_python/services/moodle_service.py src/moodle_python/services/google_docs_service.py src/moodle_python/utils/file_loader.py
venv/bin/python scripts/run_harness.py
```

For Open Skill structure validation:

```bash
venv/bin/python /home/khalid/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## External Services

The Moodle, OpenAI, and Google Docs workflows require credentials and network access. Local tests should not call external services unless the user explicitly asks for an end-to-end run.
