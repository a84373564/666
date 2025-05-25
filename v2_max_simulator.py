# v2_max_simulator.py
# 真實市場模擬器 - DOGEUSDT（含滑價、延遲、爆倉、手續費）

import json
import time
import requests
from pathlib import Path
from datetime import datetime

MODULE_PATH = Path("~/456-main/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/simulated_result.json").expanduser()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def fetch_klines(symbol="DOGEUSDT", interval="1m", limit=150):
    url = "https://api.mexc.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    return requests.get(url, params=params).json()

def simulate_trade(entry_price, tp_pct, sl_pct, candles, slippage=0.002, latency=150, fee_pct=0.001):
    for k in candles:
        time.sleep(latency / 1000)
        high = float(k[2])
        low = float(k[3])

        if high >= entry_price * (1 + tp_pct):
            exit_price = entry_price * (1 + tp_pct - slippage)
            exit_price -= exit_price * fee_pct
            return exit_price, "TP"

        elif low <= entry_price * (1 - sl_pct):
            exit_price = entry_price * (1 - sl_pct - slippage)
            exit_price -= exit_price * fee_pct
            return exit_price, "SL"

    exit_price = entry_price * (1 - slippage)
    exit_price -= exit_price * fee_pct
    return exit_price, "Timeout"

def simulate():
    module = load_json(MODULE_PATH)
    capital = module.get("capital", 70.51)
    params = module.get("parameters", {})
    tp = params.get("tp_pct", 3.0) / 100
    sl = params.get("sl_pct", 2.0) / 100

    klines = fetch_klines()
    closes = [float(k[4]) for k in klines]
    trades, wins, losses = 0, 0, 0
    peak = capital
    drawdown = 0.0

    for i in range(20, len(closes) - 20, 5):
        entry_price = closes[i]
        exit_price, outcome = simulate_trade(entry_price, tp, sl, klines[i+1:i+21])
        pnl = exit_price - entry_price
        capital += pnl
        trades += 1
        if pnl > 0:
            wins += 1
        else:
            losses += 1
        peak = max(peak, capital)
        dd = (peak - capital) / peak
        drawdown = max(drawdown, dd)
        if capital <= 10:
            print("[V2] 爆倉！資金過低")
            break

    return_pct = round((capital - module["capital"]) / module["capital"] * 100, 2)
    win_rate = round(wins / trades * 100, 2) if trades > 0 else 0.0

    result = {
        "return_pct": return_pct,
        "sharpe": round(return_pct / (drawdown * 100 + 1e-6), 2),
        "drawdown": round(drawdown * 100, 2),
        "win_rate": win_rate,
        "trade_count": trades
    }

    module["result"] = result
    module["last_simulated_at"] = datetime.utcnow().isoformat()
    save_json(module, MODULE_PATH)
    save_json(result, RESULT_PATH)
    print(f"[V2-MAX] 報酬 {return_pct}%, 勝率 {win_rate}%, 回撤 {drawdown*100:.2f}%")

if __name__ == "__main__":
    simulate()
