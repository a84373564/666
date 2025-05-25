from pathlib import Path
import json
from datetime import datetime

MODULE_PATH = Path("~/456-main/king_module.json").expanduser()
EVOLUTION_LOG_PATH = Path("~/456-main/king_evolution_log.json").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def evolve_strategy(module):
    result = module.get("result", {})
    return_pct = result.get("return_pct", 0.0)
    win_rate = result.get("win_rate", 0.0)

    # 如果缺參數就補
    if "parameters" not in module:
        module["parameters"] = {
            "ma_fast": 10,
            "ma_slow": 30,
            "sl_pct": 1.5,
            "tp_pct": 2.5
        }

    evolution_note = ""

    if return_pct < 0:
        module["parameters"]["tp_pct"] += 0.5
        module["parameters"]["sl_pct"] -= 0.2
        evolution_note = "增加止盈比，降低止損容忍度"
    elif win_rate < 50:
        module["parameters"]["ma_fast"] += 1
        module["parameters"]["ma_slow"] -= 1
        evolution_note = "調整均線參數以適應短期趨勢"

    module["generation"] = module.get("generation", 0) + 1
    module["live_rounds"] = module.get("live_rounds", 0) + 1
    module["evolution_intent"] = "self-adjust"
    module["notes"] = evolution_note
    module["updated_at"] = datetime.utcnow().isoformat()

    return module

def main():
    print("[V3] 模組進化中 → v3_evolution_engine.py")

    king = load_json(MODULE_PATH)
    evolved = evolve_strategy(king)

    save_json(MODULE_PATH, evolved)

    if EVOLUTION_LOG_PATH.exists():
        history = load_json(EVOLUTION_LOG_PATH)
    else:
        history = []

    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "generation": evolved["generation"],
        "note": evolved.get("notes", ""),
        "return_pct": evolved.get("result", {}).get("return_pct"),
        "win_rate": evolved.get("result", {}).get("win_rate"),
    })
    save_json(EVOLUTION_LOG_PATH, history)

    print(f"[V3] 進化完成：第 {evolved['generation']} 代，說明：{evolved.get('notes', '')}")

main()
