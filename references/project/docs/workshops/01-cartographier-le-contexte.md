# Atelier 01 - Cartographier le contexte

## Objectif

Transformer le projet existant en carte de contexte lisible.

## Point de depart

- `scripts/generation_moodle.py`
- `assets/prompts/system/pedagogie_moodle.txt`
- `assets/prompts/metier/geometrie_seconde.yaml`
- `src/moodle_python/services/openai_service.py`
- `src/moodle_python/services/moodle_service.py`

## Deroule

1. Identifier toutes les informations donnees au modele.
2. Classer chaque information dans une couche : systeme, metier, format, rendu, execution, evaluation.
3. Reperer les contraintes qui viennent de Moodle et non du modele.
4. Reperer les contraintes qui devraient etre verifiees par du code.
5. Completer `references/project/docs/context-engineering/context-map.md`.

## Questions de debrief

- Quelle contrainte est trop importante pour rester uniquement dans le prompt ?
- Quelle information est dupliquee ?
- Quelle information manque pour evaluer la qualite ?
