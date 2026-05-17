# Workflow - Generation Moodle

## Objectif

Generer une formation avec OpenAI, produire les quiz XML, puis publier le livre dans Moodle.

## Preconditions

- Le fichier `.env` existe.
- Les variables Moodle sont renseignees :
  - `MOODLE_URL`
  - `MOODLE_TOKEN`
  - `COURSE_ID`
- La cle OpenAI est renseignee :
  - `OPENAI_API_KEY`
- L'environnement Python est pret :

```bash
venv/bin/python -m pip install -e '.[dev]'
```

## Lancement

```bash
python3 scripts/generation_moodle.py
```

Le script bascule automatiquement vers `venv/bin/python` si le dossier `venv/` existe.

## Sorties attendues

- `output/formation_geometrie.json`
- `output/quiz_chapter_*.xml`
- Un livre Moodle publie dans le cours configure par `COURSE_ID`

## Controle rapide

```bash
venv/bin/python -m pytest
```

## Points de diagnostic

- Erreur `OPENAI_API_KEY` : verifier `.env`.
- Erreur Moodle HTTP : verifier `MOODLE_URL`, `MOODLE_TOKEN` et les permissions du token.
- JSON invalide : verifier le prompt metier et le contrat dans `prompts/contracts/course_schema.md`.
- Template introuvable : verifier `MOODLE_PAGE_TEMPLATE_PATH` ou le fichier `prompts/templates/moodle_book_chapter_template.html`.
