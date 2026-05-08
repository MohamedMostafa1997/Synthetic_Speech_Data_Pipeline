import json
import yaml
from pathlib import Path


def load_config(path: str = "config/config.yaml"):
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def ensure_directories(config):
    for directory in config["output_dirs"].values():
        Path(directory).mkdir(parents=True, exist_ok=True)

    Path("logs").mkdir(exist_ok=True)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)