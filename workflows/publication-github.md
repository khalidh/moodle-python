# Workflow - Publication GitHub

## Objectif

Publier le projet sur GitHub sans exposer les secrets locaux.

## A ne jamais publier

Ces chemins doivent rester ignores par Git :

- `.env`
- `secrets/`
- `venv/`
- `output/`
- `__pycache__/`
- `.pytest_cache/`

Le fichier partageable est `.env.example`, pas `.env`.

## Verification avant commit

```bash
git status --short --ignored
```

Verifier que les secrets apparaissent avec `!!`, par exemple :

```text
!! .env
!! secrets/
!! venv/
```

## Initialiser le depot local

```bash
git init
git branch -M main
git add .
git status --short
git commit -m "Initial Moodle generation project"
```

## Creer le depot GitHub

Creer un nouveau depot vide sur GitHub, sans README, sans `.gitignore` et sans licence si ces fichiers existent deja localement.

Puis lier le depot distant :

```bash
git remote add origin git@github.com:VOTRE_COMPTE/moodle-python.git
git push -u origin main
```

Variante HTTPS :

```bash
git remote add origin https://github.com/VOTRE_COMPTE/moodle-python.git
git push -u origin main
```

## Controle apres push

Sur GitHub, verifier que ces fichiers n'apparaissent pas :

- `.env`
- `secrets/google/credentials.json`
- `secrets/google/token.pickle`
- `venv/`
- `output/formation_geometrie.json`

## Si un secret a ete publie par erreur

1. Revoquer immediatement la cle ou le token concerne.
2. Supprimer le fichier du suivi Git.
3. Nettoyer l'historique si necessaire.
4. Regenerer une nouvelle cle.

