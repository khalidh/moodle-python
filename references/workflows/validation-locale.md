# Workflow - Validation locale

## Objectif

Verifier la structure du projet sans appeler OpenAI, Moodle ou Google Docs.

## Quand l'utiliser

- Avant une demonstration.
- Apres une modification du code.
- Apres une modification des prompts ou exemples.
- Pendant un atelier, pour montrer la difference entre validation locale et execution distante.

## Commandes

Verifier les tests :

```bash
venv/bin/python -m pytest
```

Verifier que l'exemple JSON est valide :

```bash
venv/bin/python -m json.tool assets/examples/formation_minimale.json
```

Verifier que les modules Python compilent :

```bash
venv/bin/python -m py_compile scripts/generation_moodle.py scripts/generation_google_docs.py src/moodle_python/config.py src/moodle_python/services/openai_service.py src/moodle_python/services/moodle_service.py src/moodle_python/services/google_docs_service.py src/moodle_python/utils/file_loader.py
```

Executer les scenarios de harness :

```bash
venv/bin/python scripts/run_harness.py
```

## Sortie attendue

Les tests doivent afficher :

```text
10 passed
```

## Interpretation

Si cette validation passe, le socle local est sain. Cela ne garantit pas que les appels OpenAI, Moodle ou Google Docs reussiront, car ces services dependent des secrets, du reseau et des permissions.
