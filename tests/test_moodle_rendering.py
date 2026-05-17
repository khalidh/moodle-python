from xml.etree import ElementTree

from moodle_python.services.moodle_service import (
    create_moodle_quiz,
    render_book_chapter_html,
    render_quiz_html,
)


def sample_chapter():
    return {
        "title": "Coordonnees",
        "content": "<h2>Cours</h2><p>Point \\(A(2, 3)\\).</p>",
        "quiz": [
            {
                "question": "Quelle est l'abscisse de \\(A(2, 3)\\) ?",
                "choices": ["\\(2\\)", "\\(3\\)", "\\(5\\)", "\\(1\\)"],
                "answer": "\\(2\\)",
                "explanation": "L'abscisse est la premiere coordonnee.",
            }
        ],
    }


def test_quiz_correction_is_hidden_in_book_html():
    html = render_quiz_html(sample_chapter())

    assert "<details>" in html
    assert "<summary><strong>Afficher la correction</strong></summary>" in html
    assert html.index("<details>") < html.index("Bonne réponse")


def test_book_chapter_template_injects_content_and_hidden_quiz():
    template = "<h1>{title}</h1>{content}{quiz_html}"

    html = render_book_chapter_html(sample_chapter(), template)

    assert "<h1>Coordonnees</h1>" in html
    assert "<h2>Cours</h2>" in html
    assert "Afficher la correction" in html


def test_create_moodle_quiz_writes_valid_xml(tmp_path):
    xml_path = create_moodle_quiz(sample_chapter(), 0, str(tmp_path))

    tree = ElementTree.parse(xml_path)
    root = tree.getroot()

    assert root.tag == "quiz"
    questions = root.findall("question")
    assert len(questions) == 1
    assert questions[0].attrib["type"] == "multichoice"

