import json

from moodle_python.services.openai_service import build_user_prompt, validate_course_json
from moodle_python.utils.file_loader import read_yaml


def test_short_prompt_example_is_loadable():
    prompt_data = read_yaml("examples/geometrie_seconde_short.yaml")

    assert prompt_data["nom"] == "geometrie_seconde_short"
    assert "formation courte" in build_user_prompt(prompt_data)


def test_minimal_course_example_matches_basic_contract():
    with open("examples/formation_minimale.json", "r", encoding="utf-8") as file:
        raw_content = file.read()

    course = validate_course_json(raw_content)

    assert course["title"]
    assert len(course["chapters"]) == 1

    chapter = course["chapters"][0]
    assert len(chapter["questions"]) == 2
    assert len(chapter["quiz"]) == 2

    for quiz_item in chapter["quiz"]:
        assert len(quiz_item["choices"]) == 4
        assert quiz_item["answer"] in quiz_item["choices"]


def test_minimal_course_example_is_strict_json():
    with open("examples/formation_minimale.json", "r", encoding="utf-8") as file:
        parsed = json.load(file)

    assert isinstance(parsed, dict)

