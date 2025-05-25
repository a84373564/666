# v1_king_initializer.py
import json
from datetime import datetime
from pathlib import Path
from v0_schema_guard import validate_and_fill

OUTPUT_PATH = Path("~/456-main/king_module.json").expanduser()

raw_module = {
    "id": "king",
    "symbol": "DOGEUSDT",
    "capital": 70.51,
    "parameters": {
        "ma_fast": 9,
        "ma_slow": 26,
        "sl_pct": 1.5,
        "tp_pct": 3.5
    },
    "created_at": datetime.utcnow().isoformat(),
    "generation": 0,
    "live_rounds": 0
}

king_module = validate_and_fill(raw_module)

with open(OUTPUT_PATH, "w") as f:
    json.dump(king_module, f, indent=2)

print(f"[V1] 模組 king 建立成功 → {OUTPUT_PATH}")
