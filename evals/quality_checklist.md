# Checklist qualite

Utiliser cette grille apres chaque generation.

## Structure

- Le fichier est un JSON valide.
- La racine contient `title`, `description`, `chapters`.
- Chaque chapitre contient `title`, `content`, `questions`, `quiz`.
- Chaque chapitre contient exactement 5 questions ouvertes.
- Chaque chapitre contient exactement 5 quiz.
- Chaque quiz contient exactement 4 choix.
- La bonne reponse correspond exactement a un des choix.

## Moodle

- Le HTML utilise seulement les balises autorisees.
- Les reponses cachees utilisent `<details>` et `<summary>`.
- Les contenus ne contiennent pas de Markdown.
- Les fichiers XML de quiz sont generes sans erreur.

## Mathematiques

- Toutes les variables sont dans `\\(...\\)` ou `\\[...\\]`.
- Aucune expression mathematique brute ne reste dans le HTML.
- Les notations sont coherentes avec le niveau seconde.

## Pedagogie

- Chaque chapitre contient cours, exemples, exercices, conseils et erreurs frequentes.
- Les exercices progressent du simple vers le plus complexe.
- Les explications sont suffisantes pour un eleve autonome.

## Exploitation en formation

- Le probleme rencontre peut etre rattache a une couche de contexte.
- L'amelioration proposee peut etre testee.
- La modification du prompt ne casse pas le contrat aval.

