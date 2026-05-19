# Contrat de sortie - Formation Moodle

Le modele doit produire uniquement un objet JSON valide.

## Racine

```json
{
  "title": "Titre de la formation",
  "description": "Description courte",
  "chapters": []
}
```

## Chapitre

```json
{
  "title": "Titre du chapitre",
  "content": "HTML compatible Moodle",
  "questions": [],
  "quiz": []
}
```

## Question ouverte

```json
{
  "question": "Question ouverte",
  "hidden_answer": "Reponse detaillee cachee"
}
```

## Question de quiz

```json
{
  "question": "Question du quiz",
  "choices": ["Choix 1", "Choix 2", "Choix 3", "Choix 4"],
  "answer": "Bonne reponse",
  "explanation": "Explication detaillee"
}
```

## Contraintes importantes

- `chapters` doit etre une liste.
- Chaque chapitre doit contenir exactement 5 questions ouvertes.
- Le nombre d'exercices par chapitre est defini dans `assets/prompts/metier/geometrie_seconde.yaml`, clé `parametres.exercises_per_chapter`.
- Le nombre de questions de quiz par chapitre est defini dans `assets/prompts/metier/geometrie_seconde.yaml`, clé `parametres.quiz_questions_per_chapter`.
- Le HTML doit rester compatible Moodle.
- Les mathematiques doivent etre encadrees avec les delimiteurs MathJax Moodle.
- Les champs `answer` et `explanation` des quiz ne contiennent pas de balise `<details>`.
- Le rendu Moodle masque `answer` et `explanation` au moment de construire le HTML.
- Le modele ne doit pas ajouter de markdown, de commentaire ou de texte autour du JSON.
