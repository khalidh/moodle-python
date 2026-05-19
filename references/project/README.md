# Moodle Python - Fil rouge Context Engineering

Ce projet sert de support fil rouge pour apprendre a concevoir une chaine de generation de formation Moodle avec l'IA.

L'objectif n'est pas seulement de generer un cours. Le projet permet de travailler les gestes de context engineering : cadrer une mission, separer les couches de contexte, contractualiser les sorties, evaluer les resultats, puis industrialiser progressivement le pipeline.

## Ce que fait le projet

- Charge un prompt systeme et un prompt metier.
- Genere une formation structuree avec l'API OpenAI.
- Valide le JSON produit.
- Genere des quiz Moodle XML.
- Publie le contenu dans un livre Moodle via les web services.
- Propose une variante archivee vers Google Docs.

## Structure

```text
.
|-- scripts/
|   `-- generation_moodle.py         # Pipeline principal vers Moodle
|-- src/
|   `-- moodle_python/
|       |-- config.py                # Configuration par variables d'environnement
|       |-- services/                # Integrations OpenAI, Moodle, Google Docs
|       `-- utils/                   # Lecture YAML/texte et sauvegarde JSON
|-- assets/prompts/
|   |-- system/                      # Role, normes et comportement global du modele
|   |-- metier/                      # Demandes pedagogiques par domaine
|   |-- templates/                   # Gabarits de rendu HTML Moodle
|   `-- contracts/                   # Schemas et contrats attendus par le pipeline
|-- assets/examples/                         # Jeux d'essai courts pour ateliers
|-- references/evals/                           # Grilles de controle qualite
|-- references/workflows/                       # Procedures operationnelles
|-- references/project/docs/
|   |-- architecture.md              # Carte technique et pedagogique du projet
|   |-- backlog-fil-rouge.md         # Progression possible pour la formation
|   |-- context-engineering/         # Supports sur les couches de contexte
|   |-- workshops/                   # Ateliers pratiques
|   `-- decisions/                   # Decisions d'architecture
|-- agents/
|   `-- openai.yaml                  # Metadonnees d'interface Open Skill
|-- SKILL.md                         # Point d'entree de la competence
`-- output/                          # Artefacts generes localement
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e '.[dev]'
cp .env.example .env
```

Renseigner ensuite les variables dans `.env`.

## Execution

Generation et publication Moodle :

```bash
python3 scripts/generation_moodle.py
```

Generation Google Docs :

```bash
python3 scripts/generation_google_docs.py
```

La documentation de cette variante est dans `references/project/docs/archives/google-docs.md`.

Tests rapides :

```bash
venv/bin/python -m pytest
```

Les procedures detaillees sont dans `references/workflows/`.

Pour publier le projet sur GitHub sans exposer `.env` ni les secrets Google, suivre `references/workflows/publication-github.md`.

## Utilisation en formation

Le parcours conseille est de partir du prompt actuel `assets/prompts/metier/geometrie_seconde.yaml`, puis de faire evoluer le projet par increments :

1. Cartographier les couches de contexte.
2. Formaliser le contrat de sortie JSON.
3. Ajouter des validations automatiques.
4. Ajouter une boucle d'evaluation qualite.
5. Refactorer le pipeline pour separer generation, controle et publication.
6. Brancher un second domaine metier pour verifier la reutilisabilite.

Les ateliers sont decrits dans `references/project/docs/workshops/`.
