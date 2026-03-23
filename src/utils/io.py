"""Lightweight JSON I/O helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path | str) -> dict[str, Any]:
    """Load JSON from disk into a dictionary."""
    source = Path(path)
    with source.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict[str, Any], path: Path | str, indent: int = 2) -> None:
    """Save dictionary data to JSON on disk."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
        f.write("\n")
