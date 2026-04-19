import time
import pandas as pd
import os
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv

# ===================================================
#   AUTO MODE TRADING BOT v1.0 - GITHUB AUTO DEPLOY
# ===================================================

# Load environment variables
load_dotenv("config.env")

# ===== CONFIG (dari environment variables) =====
API_KEY    = os.getenv("API_KEY", "xxx")
API_SECRET = os.getenv("API_SECRET", "xxx")

SYMBOL    = "CLUSDT"
TIMEFRAME = "15m"
LIMIT     = 100

USDT_SIZE = 25

TP_PCT = 0.02
SL_PCT = 0.015

MIN_SCORE     = 60
BAND_SIDEWAYS = 0.02
COOLDOWN      = 900

BOT_TOKEN = os.getenv("BOT_TOKEN", "xxx")
CHAT_ID   = os.getenv("CHAT_ID", "xxx")

# ===== INIT CLIENT =====
try:
    client = Client(API_KEY, API_SECRET)
    print("✅ Binance client initialized")
except Exception as e:
    print(f"❌ Binance client error: {e}")
    exit(1)

# ===== PRECISION =====
def get_symbol_info(symbol):
    info = client.futures_exchange_info()
    for s in info["symbols"]:
        if s["symbol"] == symbol:
            return s

symbol_info    = get_symbol_info(SYMBOL)
qty_precision  = symbol_info["quantityPrecision"]
price_precision = symbol_info["pricePrecision"]

def format_qty(qty):
    return float(f"{qty:.{qty_precision}f}")

def format_price(price):
    return float(f"{price:.{price_precision}f}")

# ===== GLOBAL =====
last_trade_time     = 0
last_status_telegram = 0
last_candle_time    = 0

# ===================================================
#   TELEGRAM
# ===================================================

def send_telegram(msg):
    try:
        import requests
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        print(f"✅ Telegram sent")
    except Exception as e:
        print(f"[Telegram Error] {e}")

# ===================================================
#   LOG TERMINAL
# ===================================================

def log_terminal(price, signal, score, grade, status, mode, reason, has_pos):
    now = datetime.now().strftime("%H:%M:%S")
    pos_str = "✅ ADA POSISI" if has_pos else "❌ Tidak ada posisi"

    print("\n" + "="*60)
    print(f"⏰ TIME       : {now}")
    print(f"📊 PAIR       : {SYMBOL}")
    print(f"💰 PRICE      : {round(price, 4)}")
    print(f"🧠 MODE       : {mode}")
    print(f"📡 SIGNAL     : {signal}")
    print(f"📌 REASON     : {reason}")
    print(f"🎯 SCORE      : {score} ({grade})")
    print(f"📊 STATUS     : {status}")
    print(f"🔒 POSITION   : {pos_str}")
    print("="*60)

# ===================================================
#   TELEGRAM STATUS (throttle 5 menit)
# ===================================================

def send_status_telegram(df, signal, score, grade, mode, reason):
    global last_status_telegram

    if time.time() - last_status_telegram < 300:
        return

    last  = df.iloc[-2]
    price = last["c"]
    ma    = last["ma"]
    upper = last["upper"]
    lower = last["lower"]

    status = "NO TRADE"
    if score >= MIN_SCORE:
        status = "READY 🚀"
    elif signal:
        status = "SKIP ⚠️"

    send_telegram(f"""
📊 AUTO MODE BOT v1.0

PAIR  : {SYMBOL}
MODE  : {mode}

PRICE : {round(price, 4)}
MA    : {round(ma, 4)}
UPPER : {round(upper, 4)}
LOWER : {round(lower, 4)}

SIGNAL: {signal}
REASON: {reason}

SCORE : {score} ({grade})
STATUS: {status}
""")

    last_status_telegram = time.time()

# ===================================================
#   DATA & INDIKATOR
# ===================================================

def get_data():
    klines = client.futures_klines(symbol=SYMBOL, interval=TIMEFRAME, limit=LIMIT)

    df = pd.DataFrame(klines, columns=[
        "time", "o", "h", "l", "c", "v",
        "ct", "qv", "n", "tbb", "tbq", "ig"
    ])

    df[["o", "h", "l", "c", "v"]] = df[["o", "h", "l", "c", "v"]].astype(float)
    return df

def add_indicator(df):
    # Bollinger Band
    df["ma"]    = df["c"].rolling(20).mean()
    df["std"]   = df["c"].rolling(20).std()
    df["upper"] = df["ma"] + (2 * df["std"])
    df["lower"] = df["ma"] - (2 * df["std"])

    # RSI
    delta       = df["c"].diff()
    gain        = delta.clip(lower=0).rolling(14).mean()
    loss        = (-delta.clip(upper=0)).rolling(14).mean()
    rs          = gain / loss
    df["rsi"]   = 100 - (100 / (1 + rs))

    # Volume rata-rata
    df["vol_ma"] = df["v"].rolling(20).mean()

    return df

# ===================================================
#   AUTO MODE SIGNAL
# ===================================================

def get_signal(df):
    last  = df.iloc[-2]

    close = last["c"]
    open_ = last["o"]
    upper = last["upper"]
    lower = last["lower"]
    ma    = last["ma"]
    rsi   = last["rsi"]

    band = (upper - lower) / close

    # MODE DETECTION
    if band < BAND_SIDEWAYS:
        mode = "SIDEWAYS"
    else:
        mode = "TRENDING"

    # SIDEWAYS: Reversal
    if mode == "SIDEWAYS":
        if close < lower and close > open_ and rsi < 40:
            return "BUY", "Reversal Bawah + RSI Oversold", mode

        if close > upper and close < open_ and rsi > 60:
            return "SELL", "Reversal Atas + RSI Overbought", mode

        return None, "Sideways Wait", mode

    # TRENDING: Breakout
    if mode == "TRENDING":
        if close > upper and close > ma and close > open_:
            return "BUY", "Breakout Up", mode

        if close < lower and close < ma and close < open_:
            return "SELL", "Breakout Down", mode

        return None, "Trending Wait", mode

# ===================================================
#   SCORE SYSTEM
# ===================================================

def calculate_score(df, signal, mode):
    last  = df.iloc[-2]
    score = 0

    close  = last["c"]
    ma     = last["ma"]
    upper  = last["upper"]
    lower  = last["lower"]
    rsi    = last["rsi"]
    volume = last["v"]
    vol_ma = last["vol_ma"]

    band = (upper - lower) / close

    # Komponen 1: Arah vs MA (25 poin)
    if signal == "BUY" and close > ma:
        score += 25
    elif signal == "SELL" and close < ma:
        score += 25

    # Komponen 2: Band width (25 poin)
    if band > BAND_SIDEWAYS:
        score += 25

    # Komponen 3: Volume (25 poin)
    if vol_ma > 0 and volume > vol_ma * 1.2:
        score += 25

    # Komponen 4: RSI alignment (25 poin)
    if signal == "BUY" and rsi < 55:
        score += 25
    elif signal == "SELL" and rsi > 45:
        score += 25

    grade = "C"
    if score >= 80:
        grade = "A"
    elif score >= 60:
        grade = "B"

    return score, grade

# ===================================================
#   CEK OPEN POSITION
# ===================================================

def has_open_position():
    try:
        positions = client.futures_position_information(symbol=SYMBOL)
        for p in positions:
            if float(p["positionAmt"]) != 0:
                return True
        return False
    except Exception as e:
        print(f"[Position Check Error] {e}")
        return False

# ===================================================
#   CEK CANDLE BARU
# ===================================================

def is_new_candle(df):
    global last_candle_time
    candle_time = int(df.iloc[-2]["time"])

    if candle_time != last_candle_time:
        last_candle_time = candle_time
        return True
    return False

# ===================================================
#   CANCEL ORDER
# ===================================================

def cancel_all_orders():
    try:
        client.futures_cancel_all_open_orders(symbol=SYMBOL)
    except Exception as e:
        print(f"[Cancel Order Error] {e}")

# ===================================================
#   EXECUTE TRADE
# ===================================================

def execute_trade(signal, price, df):
    global last_trade_time

    # Cek cooldown
    if time.time() - last_trade_time < COOLDOWN:
        remaining = int(COOLDOWN - (time.time() - last_trade_time))
        print(f"⏳ Cooldown aktif, tunggu {remaining}s lagi")
        return

    # Cek posisi aktif
    if has_open_position():
        print("⚠️ Ada posisi aktif, skip entry")
        return

    # Cek candle baru
    if not is_new_candle(df):
        print("⏸️ Bukan candle baru, skip entry")
        return

    cancel_all_orders()
    time.sleep(0.3)

    qty  = format_qty(USDT_SIZE / price)
    side = "BUY" if signal == "BUY" else "SELL"

    # Entry market
    client.futures_create_order(
        symbol=SYMBOL,
        side=side,
        type="MARKET",
        quantity=qty
    )

    # Hitung TP & SL
    if signal == "BUY":
        tp        = format_price(price * (1 + TP_PCT))
        sl        = format_price(price * (1 - SL_PCT))
        exit_side = "SELL"
    else:
        tp        = format_price(price * (1 - TP_PCT))
        sl        = format_price(price * (1 + SL_PCT))
        exit_side = "BUY"

    # Take Profit
    client.futures_create_order(
        symbol=SYMBOL,
        side=exit_side,
        type="TAKE_PROFIT_MARKET",
        stopPrice=tp,
        closePosition=True
    )

    # Stop Loss
    client.futures_create_order(
        symbol=SYMBOL,
        side=exit_side,
        type="STOP_MARKET",
        stopPrice=sl,
        closePosition=True
    )

    rr_ratio = round(TP_PCT / SL_PCT, 2)

    send_telegram(f"""
🚀 ENTRY {signal}

PAIR  : {SYMBOL}
PRICE : {price}

TP    : {tp}  (+{TP_PCT*100}%)
SL    : {sl}  (-{SL_PCT*100}%)
R/R   : 1:{rr_ratio}

QTY   : {qty}
SIZE  : ${USDT_SIZE}
""")

    last_trade_time = time.time()

# ===================================================
#   MAIN LOOP
# ===================================================

def run_bot():
    send_telegram(f"""
🤖 AUTO MODE BOT v1.0 STARTED (GitHub Actions)

PAIR     : {SYMBOL}
TF       : {TIMEFRAME}
SIZE     : ${USDT_SIZE}
TP       : {TP_PCT*100}%
SL       : {SL_PCT*100}%
MIN SCORE: {MIN_SCORE}
COOLDOWN : {COOLDOWN}s

⏱️ Will run for 23 hours then restart
""")

    while True:
        try:
            df = add_indicator(get_data())

            signal, reason, mode = get_signal(df)

            price = df.iloc[-1]["c"]

            if signal:
                score, grade = calculate_score(df, signal, mode)
                status = "READY 🚀" if score >= MIN_SCORE else "SKIP ⚠️"
            else:
                score, grade = 0, "-"
                status = "NO TRADE"

            has_pos = has_open_position()

            log_terminal(price, signal, score, grade, status, mode, reason, has_pos)
            send_status_telegram(df, signal, score, grade, mode, reason)

            if signal and score >= MIN_SCORE and not has_pos:
                send_telegram(
                    f"📢 SIGNAL {signal} | {mode}\n"
                    f"SCORE : {score} ({grade})\n"
                    f"REASON: {reason}"
                )
                execute_trade(signal, price, df)

            time.sleep(10)

        except Exception as e:
            print(f"[ERROR] {e}")
            send_telegram(f"❌ ERROR: {e}")
            time.sleep(15)

# ===== RUN =====
if __name__ == "__main__":
    run_bot()
