import json
import logging
from typing import Any, Dict

from openai import OpenAI


logger = logging.getLogger("generation_moodle")


def format_prompt_parameter(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def flatten_prompt_parameters(data: Dict[str, Any]) -> Dict[str, str]:
    parameters = data.get("parametres", {})
    if not isinstance(parameters, dict):
        raise ValueError("La clé 'parametres' du YAML métier doit être un objet si elle est présente.")
    return {key: format_prompt_parameter(value) for key, value in parameters.items()}


def build_user_prompt(prompt_data: Dict[str, Any]) -> str:
    prompt = prompt_data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Le YAML métier doit contenir une clé 'prompt' non vide.")

    for key, value in flatten_prompt_parameters(prompt_data).items():
        prompt = prompt.replace("{{" + key + "}}", value)

    return prompt.strip()


def generate_content(
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float,
    api_key: str,
) -> str:
    logger.info("Appel OpenAI : modèle=%s temperature=%s", model, temperature)
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
    except Exception as exc:
        logger.exception("Erreur lors de l'appel OpenAI.")
        raise RuntimeError("Échec de l'appel OpenAI") from exc

    if not response.choices:
        raise ValueError("Aucune réponse reçue de l'API OpenAI.")

    content = response.choices[0].message.content
    if not content:
        raise ValueError("La réponse OpenAI est vide.")

    logger.info("Réponse OpenAI reçue.")
    return content


def validate_course_json(content: str) -> Dict[str, Any]:
    try:
        course_json = json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("Le contenu OpenAI n'est pas un JSON valide : %s", exc)
        raise

    if not isinstance(course_json, dict):
        raise ValueError("Le JSON généré doit être un objet racine.")

    if "chapters" not in course_json or not isinstance(course_json["chapters"], list):
        raise ValueError("Le JSON doit contenir une clé 'chapters' de type liste.")

    logger.info("JSON validé avec succès, %d chapitres détectés.", len(course_json["chapters"]))
    return course_json


def normalize_mathjax(text: str) -> str:
    return text


def normalize_course_data(course_json: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(course_json, dict):
        raise TypeError("Le contenu JSON doit être un objet.")

    course_json["title"] = normalize_mathjax(str(course_json.get("title", "")))
    course_json["description"] = normalize_mathjax(str(course_json.get("description", "")))

    chapters = course_json.get("chapters")
    if not isinstance(chapters, list):
        raise ValueError("La clé 'chapters' doit être une liste dans le JSON.")

    for chapter in chapters:
        chapter["title"] = normalize_mathjax(str(chapter.get("title", "")))
        chapter["content"] = normalize_mathjax(str(chapter.get("content", "")))
        quiz_items = chapter.get("quiz", [])
        if not isinstance(quiz_items, list):
            raise ValueError("La clé 'quiz' de chaque chapitre doit être une liste.")

        for question in quiz_items:
            question["question"] = normalize_mathjax(str(question.get("question", "")))
            question["answer"] = normalize_mathjax(str(question.get("answer", "")))
            question["explanation"] = normalize_mathjax(str(question.get("explanation", "")))
            question["choices"] = [normalize_mathjax(str(choice)) for choice in question.get("choices", [])]

    return course_json
