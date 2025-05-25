# v1_king_initializer.py

import json
from datetime import datetime
from v0_schema_guard import validate_and_fill

OUTPUT_PATH = Path("~/456-main/king_module.json").expanduser()

# 初始策略與模組設定
raw_module = {
    "id": "king",
    "symbol": "DOGEUSDT",
    "capital": 70.51,
    "strategy": {
        "ma_fast": 9,
        "ma_slow": 26,
        "sl_pct": 1.5,
        "tp_pct": 3.2
    },
    "created_at": datetime.utcnow().isoformat()
}

# 套用 V0 欄位補齊與驗證
king_module = validate_and_fill(raw_module)

# 寫入 JSON 檔案
with open(OUTPUT_PATH, "w") as f:
    json.dump(king_module, f, indent=2)

print(f"[V1] 模組 king 已成功建立並寫入：{OUTPUT_PATH}")
