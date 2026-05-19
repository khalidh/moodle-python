# Workflow - Generation Google Docs

## Objectif

Utiliser la variante archivee du projet pour generer une formation et la publier dans Google Docs.

## Statut

Ce workflow est secondaire. Le flux principal du projet reste Moodle.

## Preconditions

- `secrets/google/credentials.json` existe.
- `.env` contient :
  - `GOOGLE_CREDENTIALS_PATH=secrets/google/credentials.json`
  - `GOOGLE_TOKEN_PATH=secrets/google/token.pickle`
  - `GOOGLE_DOC_TITLE=...`
- Les API Google Docs et Google Drive sont activees dans Google Cloud.

## Lancement

```bash
python3 scripts/generation_google_docs.py
```

## Sorties attendues

- `output/formation_geometrie_google_docs.json`
- Un document Google Docs cree
- Une URL affichee dans le terminal

## Documentation detaillee

Voir `references/project/docs/archives/google-docs.md`.

