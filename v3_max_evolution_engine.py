# v3_max_evolution_engine.py
# MAX 進化引擎：策略突變、自我評估、人格調整、進化紀錄

import json
from datetime import datetime
from pathlib import Path

MODULE_PATH = Path("~/456-main/king_module.json").expanduser()
LOG_PATH = Path("~/456-main/evolution_log.json").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def evolve(module):
    r = module.get("result", {})
    win_rate = r.get("win_rate", 0)
    return_pct = r.get("return_pct", 0)

    params = module.get("parameters", {})
    note = ""

    # 模擬簡易突變邏輯（可擴充為 AI 強化）
    if return_pct < 0:
        params["tp_pct"] += 0.3
        params["sl_pct"] -= 0.2
        note = "報酬為負，拉高止盈縮小止損"
    elif win_rate < 50:
        params["ma_fast"] += 1
        params["ma_slow"] -= 1
        note = "勝率過低，調整均線結構"
    else:
        params["tp_pct"] += 0.1
        note = "表現穩定，微幅增加獲利範圍"

    # 更新模組狀態
    module["parameters"] = params
    module["generation"] += 1
    module["live_rounds"] += 1
    module["evolution_intent"] = "adaptive_strengthening"
    module["notes"] = note
    module["updated_at"] = datetime.utcnow().isoformat()

    return module, note

def log_evolution(history_path, module, note):
    if history_path.exists():
        history = load_json(history_path)
    else:
        history = []

    record = {
        "generation": module["generation"],
        "timestamp": datetime.utcnow().isoformat(),
        "return_pct": module.get("result", {}).get("return_pct"),
        "win_rate": module.get("result", {}).get("win_rate"),
        "note": note
    }
    history.append(record)
    save_json(history, history_path)

def main():
    module = load_json(MODULE_PATH)
    evolved, note = evolve(module)
    save_json(evolved, MODULE_PATH)
    log_evolution(LOG_PATH, evolved, note)
    print(f"[V3-MAX] 進化完成 → 第 {evolved['generation']} 代：{note}")

if __name__ == "__main__":
    main()
