"""Lightweight YAML configuration loader for the agent package."""

from __future__ import annotations

import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "evaluation": {"timeout": 30, "mode": "peer"},
    "model": {"max_retries": 2, "response_format": "letter"},
    "analytics": {"enable_anova": True, "export_format": "csv"},
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def _parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    try:
        return int(raw)
    except ValueError:
        return raw.strip('"')


def load_config(path: str = CONFIG_PATH) -> Dict[str, Any]:
    """Parse the configuration file into a dictionary."""

    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()

    data: Dict[str, Any] = {}
    current = None
    with open(path, "r") as fh:
        for line in fh:
            line = line.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            key_val = line.strip()
            if key_val.endswith(":"):
                key = key_val[:-1]
                if indent == 0 and key == "agents":
                    continue  # root section
                elif indent == 2:
                    current = key
                    data[current] = {}
            else:
                if current is None:
                    continue
                key, val = map(str.strip, key_val.split(":", 1))
                data[current][key] = _parse_value(val)
    return {**DEFAULT_CONFIG, **data}
