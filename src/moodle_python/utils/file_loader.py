import json
import os
from typing import Any, Dict

import yaml


def read_text(path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_yaml(path: str) -> Dict[str, Any]:
    content = read_text(path)
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"Le fichier YAML doit contenir un objet racine : {path}")
    return data


def save_json(data: Dict[str, Any], output_dir: str, file_name: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return output_path
