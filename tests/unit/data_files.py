"""Builders of JSON data files for the integration and end-to-end tests."""

import json
from pathlib import Path


def project_entry(**overrides: str) -> dict[str, str]:
    entry = {
        "title": "Weather app",
        "type": "Web app",
        "description": "Shows the weather of a city.",
        "img_url": "https://example.com/weather.png",
        "source_code_url": "https://example.com/weather",
    }
    return entry | overrides


def profile_document(**overrides: object) -> dict[str, object]:
    document: dict[str, object] = {
        "name": "Ada Lovelace",
        "headline": "Software developer",
        "summary": "Builds small, tested programs.",
        "skills": ["Python", "Testing"],
        "links": [{"label": "GitHub", "url": "https://example.com/me"}],
    }
    return document | overrides


def write_json(path: Path, document: object) -> Path:
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return path
