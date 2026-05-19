# Architecture du projet

## Intention

Le projet montre comment transformer un besoin pedagogique en artefacts Moodle exploitables. Il sert aussi d'exemple concret pour enseigner le context engineering : le comportement du modele depend de plusieurs couches de contexte, pas d'un seul "gros prompt".

## Pipeline actuel

```text
prompt systeme + prompt metier
        |
        v
OpenAI genere un JSON de formation
        |
        v
validation JSON + normalisation
        |
        v
sauvegarde output/formation_geometrie.json
        |
        v
generation des quiz Moodle XML
        |
        v
publication dans un livre Moodle
```

## Couches de contexte

- Contexte systeme : `assets/prompts/system/pedagogie_moodle.txt`
- Contexte metier : `assets/prompts/metier/geometrie_seconde.yaml`
- Contexte de format : `assets/prompts/contracts/course_schema.md`
- Contexte de rendu : `assets/prompts/templates/moodle_book_chapter_template.html`
- Contexte d'execution : `.env`
- Contexte d'evaluation : `references/evals/quality_checklist.md`
- Exemples stables : `assets/examples/`
- Procedures operationnelles : `references/workflows/`

## Responsabilites des modules

- `scripts/generation_moodle.py` orchestre le pipeline.
- `src/moodle_python/config.py` lit les variables d'environnement et construit les settings.
- `src/moodle_python/services/openai_service.py` appelle le modele et valide le JSON minimal.
- `src/moodle_python/services/moodle_service.py` genere le XML Moodle et publie le livre.
- `src/moodle_python/services/google_docs_service.py` conserve une sortie alternative vers Google Docs.
- `src/moodle_python/utils/file_loader.py` gere les lectures/ecritures de fichiers.

## Prochaines evolutions pedagogiques

- Ajouter une validation structurelle plus stricte.
- Separer generation, evaluation et publication en commandes distinctes.
- Utiliser les jeux d'essai courts de `assets/examples/` pour ne pas consommer l'API pendant chaque atelier.
- Produire plusieurs prompts metier pour tester la reutilisabilite du cadre.
