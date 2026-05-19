import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List
from xml.etree import ElementTree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from moodle_python.services.moodle_service import create_moodle_quiz, render_book_chapter_html
from moodle_python.services.openai_service import build_user_prompt, normalize_course_data, validate_course_json
from moodle_python.utils.file_loader import read_text, read_yaml


DEFAULT_SCENARIOS_DIR = PROJECT_ROOT / "harness" / "scenarios"
DEFAULT_TEMPLATE_PATH = PROJECT_ROOT / "assets" / "prompts" / "templates" / "moodle_book_chapter_template.html"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "output" / "harness_report.json"


class HarnessFailure(AssertionError):
    pass


def project_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def load_json_file(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Fixture JSON introuvable : {path}")
    return path.read_text(encoding="utf-8")


def require_equal(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise HarnessFailure(f"{label}: attendu {expected!r}, reçu {actual!r}")


def require_fragments(label: str, text: str, fragments: Iterable[str]) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise HarnessFailure(f"{label}: fragments absents: {missing}")


def validate_chapter_counts(course: Dict[str, Any], expect: Dict[str, Any]) -> None:
    chapters = course.get("chapters", [])
    if "chapter_count" in expect:
        require_equal("chapter_count", len(chapters), expect["chapter_count"])

    for index, chapter in enumerate(chapters, start=1):
        if "quiz_questions_per_chapter" in expect:
            require_equal(
                f"chapter_{index}.quiz_count",
                len(chapter.get("quiz", [])),
                expect["quiz_questions_per_chapter"],
            )
        if "open_questions_per_chapter" in expect:
            require_equal(
                f"chapter_{index}.open_question_count",
                len(chapter.get("questions", [])),
                expect["open_questions_per_chapter"],
            )


def run_scenario(scenario_path: Path, template: str) -> Dict[str, Any]:
    scenario = read_yaml(str(scenario_path))
    name = str(scenario.get("name") or scenario_path.stem)
    expect = scenario.get("expect", {})
    if not isinstance(expect, dict):
        raise HarnessFailure("La clé 'expect' doit être un objet.")

    prompt_path = project_path(str(scenario["prompt_path"]))
    course_path = project_path(str(scenario["course_json_path"]))

    prompt = build_user_prompt(read_yaml(str(prompt_path)))
    require_fragments("prompt", prompt, expect.get("required_prompt_fragments", []))

    course = validate_course_json(load_json_file(course_path))
    course = normalize_course_data(course)

    if "title" in expect:
        require_equal("title", course.get("title"), expect["title"])
    validate_chapter_counts(course, expect)

    content_html = "\n".join(str(chapter.get("content", "")) for chapter in course.get("chapters", []))
    require_fragments("content_html", content_html, expect.get("required_content_fragments", []))

    rendered_html = "\n".join(render_book_chapter_html(chapter, template) for chapter in course.get("chapters", []))
    require_fragments("rendered_html", rendered_html, expect.get("required_rendered_html_fragments", []))

    xml_fragments = expect.get("required_xml_fragments", [])
    with tempfile.TemporaryDirectory(prefix="moodle_harness_") as tmp_dir:
        xml_paths = [
            create_moodle_quiz(chapter, index, tmp_dir)
            for index, chapter in enumerate(course.get("chapters", []))
        ]
        xml_paths = [path for path in xml_paths if path]
        xml_text = "\n".join(Path(path).read_text(encoding="utf-8") for path in xml_paths)
        require_fragments("moodle_xml", xml_text, xml_fragments)
        for xml_path in xml_paths:
            ElementTree.parse(xml_path)

    return {
        "name": name,
        "path": str(scenario_path.relative_to(PROJECT_ROOT)),
        "status": "passed",
        "chapters": len(course.get("chapters", [])),
        "quiz_questions": sum(len(chapter.get("quiz", [])) for chapter in course.get("chapters", [])),
    }


def discover_scenarios(scenario_args: List[str]) -> List[Path]:
    if scenario_args:
        return [project_path(path) for path in scenario_args]
    return sorted(DEFAULT_SCENARIOS_DIR.glob("*.yaml"))


def write_report(path: Path, report: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Moodle Python harness scenarios.")
    parser.add_argument("--scenario", action="append", default=[], help="Scenario YAML path. Can be used multiple times.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH), help="JSON report output path.")
    args = parser.parse_args()

    scenarios = discover_scenarios(args.scenario)
    if not scenarios:
        print("No harness scenarios found.", file=sys.stderr)
        return 2

    template = read_text(str(DEFAULT_TEMPLATE_PATH))
    results = []
    passed = 0

    for scenario_path in scenarios:
        try:
            result = run_scenario(scenario_path, template)
            passed += 1
            print(f"PASS {result['name']}")
        except Exception as exc:
            result = {
                "name": scenario_path.stem,
                "path": str(scenario_path.relative_to(PROJECT_ROOT)) if scenario_path.is_relative_to(PROJECT_ROOT) else str(scenario_path),
                "status": "failed",
                "error": str(exc),
            }
            print(f"FAIL {result['name']}: {exc}", file=sys.stderr)
        results.append(result)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "passed" if passed == len(results) else "failed",
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
        },
        "results": results,
    }
    write_report(project_path(args.report), report)
    print(f"Report written to {args.report}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
