# Atelier 02 - Contractualiser la sortie

## Objectif

Passer d'une consigne de generation a un contrat exploitable par le code.

## Point de depart

- `prompts/contracts/course_schema.md`
- `examples/formation_minimale.json`
- `src/moodle_python/services/openai_service.py`
- `evals/quality_checklist.md`

## Deroule

1. Lire la structure JSON attendue.
2. Comparer le contrat avec le prompt metier.
3. Comparer le contrat avec ce que valide actuellement `validate_course_json`.
4. Lister les validations manquantes.
5. Ajouter progressivement des controles automatiques.

## Validations candidates

- Nombre minimal de chapitres.
- Presence de `questions` et `quiz`.
- Nombre exact de questions par chapitre.
- Nombre exact de choix par quiz.
- Correspondance exacte entre `answer` et un element de `choices`.

## Debrief

Le prompt demande une forme. Le contrat permet au logiciel de refuser une forme invalide. C'est un passage cle du context engineering vers l'engineering tout court.
