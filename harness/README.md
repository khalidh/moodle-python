# Harness

This folder contains deterministic checks for the Moodle Python skill and pipeline.

The harness does not call OpenAI, Moodle, or Google Docs. It validates local fixtures, prompt rendering, JSON structure, Moodle HTML rendering, and Moodle XML generation.

## Run

```bash
venv/bin/python scripts/run_harness.py
```

By default, the report is written to:

```text
output/harness_report.json
```

Use a custom report path:

```bash
venv/bin/python scripts/run_harness.py --report output/custom_harness_report.json
```

Run one scenario:

```bash
venv/bin/python scripts/run_harness.py --scenario harness/scenarios/minimal_course.yaml
```

## Scenario Format

Each scenario is a YAML file with:

- `name`: stable scenario identifier.
- `prompt_path`: YAML prompt fixture to render.
- `course_json_path`: JSON course fixture to validate and render.
- `expect`: expected counts and required fragments.

Keep scenarios short and deterministic. Use them to catch regressions in contracts, paths, prompt rendering, and Moodle export behavior.
