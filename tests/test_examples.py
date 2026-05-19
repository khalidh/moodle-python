import json

from moodle_python.services.openai_service import build_user_prompt, validate_course_json
from moodle_python.utils.file_loader import read_yaml


def test_short_prompt_example_is_loadable():
    prompt_data = read_yaml("assets/examples/geometrie_seconde_short.yaml")

    assert prompt_data["nom"] == "geometrie_seconde_short"
    assert "formation courte" in build_user_prompt(prompt_data)


def test_prompt_parameters_are_injected():
    prompt = build_user_prompt(
        {
            "parametres": {
                "quiz_questions_per_chapter": 10,
                "exercises_per_chapter": 10,
            },
            "prompt": (
                "Créer {{quiz_questions_per_chapter}} questions de quiz "
                "et {{exercises_per_chapter}} exercices."
            ),
        }
    )

    assert prompt == "Créer 10 questions de quiz et 10 exercices."


def test_prompt_list_parameters_are_injected_as_bullets():
    prompt = build_user_prompt(
        {
            "parametres": {"chapter_plan": ["Chapitre A", "Chapitre B"]},
            "prompt": "Plan :\n{{chapter_plan}}",
        }
    )

    assert prompt == "Plan :\n- Chapitre A\n- Chapitre B"


def test_geometrie_prompt_uses_externalized_course_context():
    prompt_data = read_yaml("assets/prompts/metier/geometrie_seconde.yaml")
    parameters = prompt_data["parametres"]
    prompt = build_user_prompt(prompt_data)

    assert parameters["prompt_name"] == "geometrie_seconde"
    assert parameters["level_code"] == "seconde_generale"
    assert parameters["subject_code"] == "mathematiques"
    assert parameters["theme_code"] == "geometrie_analytique"
    assert 'Créer la formation "Géométrie analytique en seconde"' in prompt
    assert "Le thème principal est : géométrie analytique." in prompt
    assert "- Repères et coordonnées dans le plan" in prompt


def test_geometrie_prompt_requires_exercises_in_content():
    prompt_data = read_yaml("assets/prompts/metier/geometrie_seconde.yaml")
    prompt = build_user_prompt(prompt_data)

    assert 'Les exercices doivent être écrits dans le champ "content"' in prompt
    assert "<h3>Exercices</h3>" in prompt
    assert "exactement 5 exercices" in prompt


def test_minimal_course_example_matches_basic_contract():
    with open("assets/examples/formation_minimale.json", "r", encoding="utf-8") as file:
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
    with open("assets/examples/formation_minimale.json", "r", encoding="utf-8") as file:
        parsed = json.load(file)

    assert isinstance(parsed, dict)
