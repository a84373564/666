# v2_market_reality_simulator.py
# 真實市場模擬器（DOGEUSDT 專用）

import json
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta

MODULE_PATH = Path("~/456-main/king_module.json").expanduser()
RESULT_PATH = Path("~/456-main/simulated_result.json").expanduser()
CONFIG_PATH = Path("~/456-main/V2_market_simulator/sim_config.json").expanduser()

# 預設模擬參數（若 config 檔不存在）
DEFAULT_CONFIG = {
    "slippage_pct": 0.002,
    "latency_ms": 150,
    "market_style": "normal",
    "fee_pct": 0.001
}

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG if 'sim_config' in str(path) else {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def fetch_doge_klines(limit=300):
    url = "https://api.mexc.com/api/v3/klines"
    params = {
        "symbol": "DOGEUSDT",
        "interval": "1m",
        "limit": limit
    }
    r = requests.get(url, params=params)
    return r.json()

def simulate_trade(entry_price, sl_pct, tp_pct, candles, slippage, fee_pct, latency):
    for i, k in enumerate(candles):
        high = float(k[2])
        low = float(k[3])
        if high >= entry_price * (1 + tp_pct):
            exit_price = entry_price * (1 + tp_pct - slippage)
            return exit_price, "TP", i + 1
        elif low <= entry_price * (1 - sl_pct):
            exit_price = entry_price * (1 - sl_pct - slippage)
            return exit_price, "SL", i + 1
        time.sleep(latency / 1000.0)
    return entry_price, "Timeout", len(candles)

def simulate():
    king = load_json(MODULE_PATH)
    config = load_json(CONFIG_PATH)

    # 固定幣種
    king["symbol"] = "DOGEUSDT"

    strategy = king.get("strategy", {})
    fast = strategy.get("ma_fast", 9)
    slow = strategy.get("ma_slow", 26)
    sl_pct = strategy.get("sl_pct", 0.02)
    tp_pct = strategy.get("tp_pct", 0.04)

    slippage = config.get("slippage_pct", 0.002)
    latency = config.get("latency_ms", 100)
    fee_pct = config.get("fee_pct", 0.001)

    candles = fetch_doge_klines(limit=200)
    closes = [float(c[4]) for c in candles]
    capital = king.get("capital", 70.51)
    trades = 0
    wins = 0
    total_return = 0.0
    max_drawdown = 0.0
    peak = capital

    for i in range(slow, len(closes) - 20, 10):
        ma_fast = sum(closes[i-fast:i]) / fast
        ma_slow = sum(closes[i-slow:i]) / slow
        price = closes[i]

        if ma_fast > ma_slow:
            exit_price, outcome, bars = simulate_trade(price, sl_pct, tp_pct, candles[i:i+20], slippage, fee_pct, latency)
            fee = (price + exit_price) * fee_pct
            pnl = exit_price - price - fee
            capital += pnl
            total_return += pnl
            trades += 1
            if pnl > 0:
                wins += 1
            if capital > peak:
                peak = capital
            drawdown = (peak - capital) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    return_pct = round((capital - king["capital"]) / king["capital"] * 100, 2)
    sharpe = round((return_pct / (max_drawdown * 100 + 1e-6)), 2)
    win_rate = round((wins / trades) * 100, 2) if trades > 0 else 0.0

    king["result"] = {
        "return_pct": return_pct,
        "sharpe": sharpe,
        "drawdown": round(max_drawdown * 100, 2),
        "win_rate": win_rate,
        "trade_count": trades
    }

    king["last_simulated_at"] = datetime.utcnow().isoformat()
    save_json(king, MODULE_PATH)
    save_json(king["result"], RESULT_PATH)

    print(f"[V2 完成] 報酬: {return_pct}%, 勝率: {win_rate}%, 策略交易: {trades} 次")

if __name__ == "__main__":
    simulate()
