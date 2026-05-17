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

from moodle_python.config import load_google_docs_settings
from moodle_python.services.google_docs_service import create_google_docs_formation
from moodle_python.services.openai_service import (
    build_user_prompt,
    generate_content,
    normalize_course_data,
    validate_course_json,
)
from moodle_python.utils.file_loader import read_text, read_yaml, save_json


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("generation_mardi_google_docs")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()


def main() -> None:
    settings = load_google_docs_settings()
    generation_settings = settings.generation
    os.makedirs(generation_settings.output_dir, exist_ok=True)

    system_prompt = read_text(generation_settings.system_prompt_path)
    metier_prompt = build_user_prompt(read_yaml(generation_settings.metier_prompt_path))

    raw_content = generate_content(
        system_prompt=system_prompt,
        user_prompt=metier_prompt,
        model=generation_settings.openai_model,
        temperature=generation_settings.openai_temperature,
        api_key=generation_settings.openai_api_key,
    )

    course_json = validate_course_json(raw_content)
    course_json = normalize_course_data(course_json)
    output_path = save_json(course_json, generation_settings.output_dir, "formation_geometrie_google_docs.json")
    logger.info("JSON sauvegardé dans %s", output_path)

    doc_url = create_google_docs_formation(
        course_json=course_json,
        credentials_path=settings.credentials_path,
        token_path=settings.token_path,
        document_title=settings.document_title,
    )
    print(f"Document Google Docs créé : {doc_url}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Le processus a échoué.")
        sys.exit(1)
