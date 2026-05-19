# Prompts

Les prompts sont separes par responsabilite.

## `system/`

Definit le role global du modele, ses normes de sortie et ses interdits generaux.

## `metier/`

Contient les demandes pedagogiques propres a une formation donnee : matiere, niveau, theme, structure attendue, contraintes didactiques.

## `templates/`

Contient les gabarits utilises apres generation pour composer le rendu Moodle, par exemple `moodle_book_chapter_template.html`.

## `contracts/`

Documente les structures attendues par le code. Un contrat doit etre suffisamment clair pour guider le prompt et suffisamment precis pour inspirer les validations automatiques.
