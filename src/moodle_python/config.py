import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    moodle_url: str
    moodle_token: str
    course_id: int
    output_dir: str
    metier_prompt_path: str
    system_prompt_path: str
    moodle_page_template_path: str


@dataclass(frozen=True)
class GenerationSettings:
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    output_dir: str
    metier_prompt_path: str
    system_prompt_path: str


@dataclass(frozen=True)
class GoogleDocsSettings:
    generation: GenerationSettings
    credentials_path: str
    token_path: str
    document_title: str


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Variable d'environnement requise manquante : {name}")
    return value


def optional_env(name: str, default: str) -> str:
    return os.getenv(name, default)


def parse_int_env(name: str) -> int:
    value = require_env(name)
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"La variable d'environnement {name} doit être un entier. Valeur reçue : {value}") from exc


def parse_float_env(name: str, default: str) -> float:
    value = optional_env(name, default)
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"La variable d'environnement {name} doit être un nombre. Valeur reçue : {value}") from exc


def load_settings() -> Settings:
    load_dotenv()
    generation_settings = load_generation_settings(load_env_file=False)
    return Settings(
        openai_api_key=generation_settings.openai_api_key,
        openai_model=generation_settings.openai_model,
        openai_temperature=generation_settings.openai_temperature,
        moodle_url=require_env("MOODLE_URL"),
        moodle_token=require_env("MOODLE_TOKEN"),
        course_id=parse_int_env("COURSE_ID"),
        output_dir=generation_settings.output_dir,
        metier_prompt_path=generation_settings.metier_prompt_path,
        system_prompt_path=generation_settings.system_prompt_path,
        moodle_page_template_path=optional_env(
            "MOODLE_PAGE_TEMPLATE_PATH",
            "assets/prompts/templates/moodle_book_chapter_template.html",
        ),
    )


def load_generation_settings(load_env_file: bool = True) -> GenerationSettings:
    if load_env_file:
        load_dotenv()
    return GenerationSettings(
        openai_api_key=require_env("OPENAI_API_KEY"),
        openai_model=optional_env("OPENAI_MODEL", "gpt-4.1-mini"),
        openai_temperature=parse_float_env("OPENAI_TEMPERATURE", "0.4"),
        output_dir=optional_env("OUTPUT_DIR", "output"),
        metier_prompt_path=optional_env(
            "METIER_PROMPT_PATH",
            optional_env("PROMPT_PATH", "assets/prompts/metier/geometrie_seconde.yaml"),
        ),
        system_prompt_path=optional_env("SYSTEM_PROMPT_PATH", "assets/prompts/system/pedagogie_moodle.txt"),
    )


def load_google_docs_settings() -> GoogleDocsSettings:
    load_dotenv()
    return GoogleDocsSettings(
        generation=load_generation_settings(load_env_file=False),
        credentials_path=optional_env("GOOGLE_CREDENTIALS_PATH", "secrets/google/credentials.json"),
        token_path=optional_env("GOOGLE_TOKEN_PATH", "secrets/google/token.pickle"),
        document_title=optional_env("GOOGLE_DOC_TITLE", "Formation - Géométrie analytique - Seconde"),
    )
