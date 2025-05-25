# v0_schema_guard.py

import json
from pathlib import Path

SCHEMA_PATH = Path("~/456-main/universal_schema.json").expanduser()

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def validate_and_fill(data):
    schema = load_schema()
    return _fill_recursive(schema, data)

def _fill_recursive(schema, data):
    if isinstance(schema, dict):
        result = {}
        for key, value in schema.items():
            if key in data:
                result[key] = _fill_recursive(value, data[key])
            else:
                result[key] = value
                print(f"[SCHEMA] 缺欄位 {key} → 已補預設值 {value}")
        return result
    else:
        return data if data is not None else schema
