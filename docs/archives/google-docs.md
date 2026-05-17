# Génération de Formation vers Google Docs

Ce script `archives/genere_mardi_google_docs.py` génère une formation de géométrie analytique en utilisant OpenAI et la publie automatiquement dans un document Google Docs.

## Prérequis

- Python 3.8+
- Clé API OpenAI
- Compte Google avec accès à Google Docs et Drive

## Installation

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration Google Docs API

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Activez l'API Google Docs et Google Drive.
4. Créez des identifiants OAuth 2.0 :
   - Type : Application de bureau
   - Téléchargez le fichier `credentials.json` et placez-le dans `secrets/google/credentials.json`.

## Variables d'environnement

Créez un fichier `.env` dans le dossier racine avec :

```
OPENAI_API_KEY=votre_clé_openai
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TEMPERATURE=0.4
METIER_PROMPT_PATH=prompts/metier/geometrie_seconde.yaml
SYSTEM_PROMPT_PATH=prompts/system/pedagogie_moodle.txt
GOOGLE_CREDENTIALS_PATH=secrets/google/credentials.json
GOOGLE_TOKEN_PATH=secrets/google/token.pickle
GOOGLE_DOC_TITLE=Formation - Géométrie analytique - Seconde
```

## Exécution

Lancez le script :

```bash
python archives/genere_mardi_google_docs.py
```

Le script va :
- Générer le contenu avec OpenAI
- Créer un document Google Docs
- Afficher l'URL du document créé

## Authentification

La première fois, le script ouvrira une fenêtre de navigateur pour l'authentification Google. Acceptez les permissions. Un fichier `secrets/google/token.pickle` sera créé pour les futures exécutions.

## Structure du document

Le document contiendra :
- Titre principal
- Introduction
- Sections pour chaque chapitre
- Contenu du cours
- Mini quiz avec questions, choix, réponses et explications
