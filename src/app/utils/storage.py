import json
from pathlib import Path


DATA_FILE = Path("data.json")

def load_pages():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}

def save_pages(pages):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=4, ensure_ascii=False)