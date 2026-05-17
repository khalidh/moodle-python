import logging
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PYTHON = os.path.join(PROJECT_ROOT, "venv", "bin", "python")
if __name__ == "__main__" and os.path.isfile(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON, *sys.argv])

SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from moodle_python.config import load_settings
from moodle_python.services.moodle_service import create_moodle_book, create_moodle_quiz
from moodle_python.services.openai_service import (
    build_user_prompt,
    generate_content,
    normalize_course_data,
    validate_course_json,
)
from moodle_python.utils.file_loader import read_text, read_yaml, save_json


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("generation_moodle")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()


def main() -> None:
    settings = load_settings()
    os.makedirs(settings.output_dir, exist_ok=True)

    system_prompt = read_text(settings.system_prompt_path)
    metier_prompt = build_user_prompt(read_yaml(settings.metier_prompt_path))
    chapter_template = read_text(settings.moodle_page_template_path)

    raw_content = generate_content(
        system_prompt=system_prompt,
        user_prompt=metier_prompt,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        api_key=settings.openai_api_key,
    )

    course_json = validate_course_json(raw_content)
    course_json = normalize_course_data(course_json)
    output_path = save_json(course_json, settings.output_dir, "formation_geometrie.json")
    logger.info("JSON sauvegardé dans %s", output_path)

    for chapter_index, chapter in enumerate(course_json.get("chapters", [])):
        create_moodle_quiz(chapter, chapter_index, settings.output_dir)

    book_id = create_moodle_book(
        course_json=course_json,
        moodle_url=settings.moodle_url,
        moodle_token=settings.moodle_token,
        course_id=settings.course_id,
        chapter_template=chapter_template,
    )
    logger.info("Livre Moodle créé avec succès, bookid=%s", book_id)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Le processus a échoué.")
        sys.exit(1)
