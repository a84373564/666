import json
from pathlib import Path

MODULE_PATH = Path("~/456-main/king_module.json").expanduser()
REPORT_PATH = Path("~/456-main/v4_insight_report.txt").expanduser()
HISTORY_PATH = Path("~/456-main/king_history.json").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def print_report(entry):
    print("──────────────────────────────────────────────")
    print(f"[回合]       {entry['live_rounds']}")
    print(f"[資金]       {entry['capital_start']} → {entry['capital_end']}  （{entry['profit_pct']}）")
    print(f"[勝率]       {entry.get('win_rate', 'N/A')}%")
    print(f"[爆倉]       {'是' if entry.get('blown_up') else '否'}")
    print(f"[分數]       {entry.get('score', 0):.1f}（等級：{entry.get('grade', 'N/A')}）")
    print(f"[標籤]       {entry.get('flags', [])}")
    print(f"[建議]       {entry.get('suggestion', '無')}")
    print("──────────────────────────────────────────────")

def generate_report():
    king = load_json(MODULE_PATH)

    capital_start = king.get("capital_start", 70.51)
    capital_end = king.get("capital_end", capital_start)
    profit_pct = (capital_end - capital_start) / capital_start * 100
    win_rate = king.get("win_rate", 0.0)
    blown_up = king.get("drawdown", 0.0) >= 100

    entry = {
        "live_rounds": king.get("live_rounds", 0),
        "capital_start": round(capital_start, 2),
        "capital_end": round(capital_end, 2),
        "profit_pct": f"{profit_pct:+.2f}%",
        "win_rate": round(win_rate, 2),
        "blown_up": blown_up,
        "score": round(king.get("score", 0.0), 1),
        "grade": king.get("grade", "N/A"),
        "flags": king.get("flags", []),
        "suggestion": king.get("suggestion", "尚未評分")
    }

    # 儲存歷史紀錄
    history = []
    if HISTORY_PATH.exists():
        history = load_json(HISTORY_PATH)
    history.append(entry)
    save_json(HISTORY_PATH, history)

    # CLI 顯示
    for record in history[-3:]:  # 顯示最近 3 筆
        print_report(record)

    # 寫入文字檔
    with open(REPORT_PATH, "w") as f:
        for record in history:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    generate_report()
