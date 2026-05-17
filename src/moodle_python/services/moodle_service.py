import logging
import os
from typing import Any, Dict

import requests
from requests.exceptions import RequestException


logger = logging.getLogger("generation_moodle")


def call_moodle(wsfunction: str, data: Dict[str, Any], moodle_url: str, moodle_token: str) -> Dict[str, Any]:
    payload = {
        "wstoken": moodle_token,
        "wsfunction": wsfunction,
        "moodlewsrestformat": "json",
        **data,
    }

    logger.info("Appel Moodle : %s", wsfunction)
    try:
        response = requests.post(moodle_url, data=payload, timeout=30)
        response.raise_for_status()
    except RequestException as exc:
        logger.exception("Erreur HTTP lors de l'appel Moodle.")
        raise RuntimeError("Échec de l'appel Moodle") from exc

    try:
        result = response.json()
    except ValueError as exc:
        logger.error("Réponse Moodle non JSON : %s", response.text)
        raise RuntimeError("Réponse Moodle non JSON") from exc

    if isinstance(result, dict) and result.get("exception"):
        logger.error("Moodle a renvoyé une exception : %s", result)
        raise RuntimeError(f"Erreur Moodle : {result.get('message', 'unknown')}")

    logger.info("Réponse Moodle reçue pour %s", wsfunction)
    return result


def render_quiz_html(chapter: Dict[str, Any]) -> str:
    quiz = chapter.get("quiz", [])
    if not quiz:
        return ""

    html = ["<h2>Mini quiz</h2>"]
    for index, question in enumerate(quiz, start=1):
        html.append(f"<h3>Question {index}</h3>")
        html.append(f"<p><strong>{question.get('question', '')}</strong></p>")
        html.append("<ul>")
        for choice in question.get("choices", []):
            html.append(f"<li>{choice}</li>")
        html.append("</ul>")
        html.append("<details>")
        html.append("<summary><strong>Afficher la correction</strong></summary>")
        html.append(f"<p><strong>Bonne réponse :</strong> {question.get('answer', '')}</p>")
        html.append(f"<p><strong>Explication :</strong> {question.get('explanation', '')}</p>")
        html.append("</details>")
    return "".join(html)


def render_book_chapter_html(chapter: Dict[str, Any], template: str) -> str:
    return template.format(
        title=chapter.get("title", "Chapitre"),
        content=chapter.get("content", ""),
        quiz_html=render_quiz_html(chapter),
    )


def wrap_cdata(text: str) -> str:
    safe_text = text.replace("]]>", "]] ]]>".replace(" ", ""))
    return f"<![CDATA[{safe_text}]]>"


def create_moodle_quiz(chapter: Dict[str, Any], chapter_index: int, output_dir: str) -> str:
    quiz_items = chapter.get("quiz", [])
    if not quiz_items:
        logger.warning("Aucun quiz trouvé pour le chapitre %d", chapter_index + 1)
        return ""

    os.makedirs(output_dir, exist_ok=True)
    file_name = f"quiz_chapter_{chapter_index + 1}.xml"
    path = os.path.join(output_dir, file_name)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]

    for question_index, question in enumerate(quiz_items, start=1):
        choices = question.get("choices", [])
        answer_text = question.get("answer", "").strip()
        correct_choice = next((choice for choice in choices if choice.strip() == answer_text), None)
        if correct_choice is None and choices:
            logger.warning(
                "Aucune correspondance exacte trouvée pour la bonne réponse du chapitre %d question %d. Première réponse utilisée.",
                chapter_index + 1,
                question_index,
            )
            correct_choice = choices[0]

        lines.append('  <question type="multichoice">')
        lines.append("    <name><text>" + wrap_cdata(f"Chapitre {chapter_index + 1} - Question {question_index}") + "</text></name>")
        question_body = f"<p><strong>{question.get('question', '')}</strong></p>"
        lines.append('    <questiontext format="html"><text>' + wrap_cdata(question_body) + "</text></questiontext>")
        lines.append('    <generalfeedback format="html"><text>' + wrap_cdata(question.get("explanation", "")) + "</text></generalfeedback>")
        lines.append("    <defaultgrade>1.0000000</defaultgrade>")
        lines.append("    <penalty>0.3333333</penalty>")
        lines.append("    <hidden>0</hidden>")
        lines.append("    <single>true</single>")
        lines.append("    <shuffleanswers>true</shuffleanswers>")
        lines.append("    <answernumbering>abc</answernumbering>")

        for choice in choices:
            fraction = "100" if choice.strip() == correct_choice.strip() else "0"
            lines.append(f'    <answer fraction="{fraction}" format="html">')
            lines.append("      <text>" + wrap_cdata(choice) + "</text>")
            feedback_text = "Bonne réponse." if fraction == "100" else "Mauvaise réponse."
            lines.append('      <feedback format="html"><text>' + wrap_cdata(feedback_text) + "</text></feedback>")
            lines.append("    </answer>")

        lines.append("  </question>")

    lines.append("</quiz>")

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    logger.info("Fichier Moodle XML généré : %s", path)
    return path


def create_moodle_book(
    course_json: Dict[str, Any],
    moodle_url: str,
    moodle_token: str,
    course_id: int,
    chapter_template: str,
) -> int:
    book_data = {
        "courseid": course_id,
        "name": course_json.get("title", "Formation géométrie analytique"),
        "intro": f"<p>{course_json.get('description', '')}</p>",
    }

    book_response = call_moodle("local_aiimport_create_book", book_data, moodle_url, moodle_token)
    book_id = book_response.get("bookid")
    if not book_id:
        raise RuntimeError("Moodle n'a pas retourné de bookid.")

    logger.info("Livre Moodle créé : bookid=%s", book_id)

    for chapter_index, chapter in enumerate(course_json.get("chapters", [])):
        chapter_html = render_book_chapter_html(chapter, chapter_template)
        logger.info("Ajout du chapitre %d : %s", chapter_index + 1, chapter.get("title", "Chapitre"))
        call_moodle(
            "local_aiimport_add_book_chapter",
            {
                "bookid": book_id,
                "title": chapter.get("title", "Chapitre"),
                "content": chapter_html,
                "subchapter": 0,
            },
            moodle_url,
            moodle_token,
        )

    return book_id
