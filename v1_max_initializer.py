# v1_max_initializer.py
# 完整人格模組初始化器

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
    "style_profile": {
        "risk_tolerance": "high",
        "emotional_tendency": "aggressive",
        "temperature_level": 0.72
    },
    "generation": 0,
    "live_rounds": 0,
    "init_bias_score": 1.0,
    "training_trace_id": "doge_mainline",
    "creation_id": "v1max_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
    "created_at": datetime.utcnow().isoformat()
}

module = validate_and_fill(raw_module)

with open(OUTPUT_PATH, "w") as f:
    json.dump(module, f, indent=2)

print(f"[V1-MAX] 模組 king 建立完成 → {OUTPUT_PATH}")
