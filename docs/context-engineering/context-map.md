# Carte de contexte

Cette carte sert a rendre visibles les informations donnees au modele et les contraintes imposees au pipeline.

## 1. Mission

Generer une formation Moodle complete a partir d'un sujet pedagogique.

Questions a poser :

- Quel public vise-t-on ?
- Quel niveau scolaire ou professionnel ?
- Quel resultat doit etre produit ?
- Quel systeme consommera le resultat ?

## 2. Role du modele

Fichier : `prompts/system/pedagogie_moodle.txt`

Le prompt systeme fixe l'identite professionnelle du modele et les regles globales : pedagogie, Moodle, JSON strict.

## 3. Contexte metier

Fichier : `prompts/metier/geometrie_seconde.yaml`

Le prompt metier porte le sujet, le niveau, le volume attendu, les contraintes HTML et les regles MathJax.

## 4. Contrat de sortie

Fichier : `prompts/contracts/course_schema.md`

Le contrat de sortie decrit la structure que le code Python attend. C'est le lien entre prompt engineering et software engineering.

## 5. Contraintes aval

Les sorties sont consommees par :

- `json.loads()` pour la validation.
- Moodle Book pour le contenu HTML.
- Moodle XML pour les quiz.
- Google Docs dans le flux archive.

## 6. Evaluation

Fichier : `evals/quality_checklist.md`

La qualite ne se limite pas a "le modele a repondu". On verifie la structure, la pedagogie, le rendu Moodle, la securite de publication et la maintenabilite.

