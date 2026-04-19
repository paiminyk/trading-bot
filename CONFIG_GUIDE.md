# ⚙️ Bot Configuration Guide

Panduan customize bot sesuai trading style Anda.

---

## 📊 Trading Parameters

### Pair & Timeframe
```python
SYMBOL = "CLUSDT"      # Binance Futures symbol
TIMEFRAME = "15m"      # Candle timeframe (1m, 5m, 15m, 1h, 4h)
LIMIT = 100            # Jumlah candle historical data
```

**Recommendation:**
- Volume pair: BTCUSDT, ETHUSDT, BNBUSDT
- Alt pair: CLUSDT, APTUSDT, SOLUSDT
- TF pendek (1m-5m): scalping, high frequency
- TF medium (15m-1h): swing trading
- TF panjang (4h+): position trading

---

## 💰 Risk Management

### Position Sizing
```python
USDT_SIZE = 25  # Dollar per trade (USDT)
```

**Guideline:**
- Ultra conservative: 5 USDT
- Conservative: 25 USDT (default)
- Moderate: 50-100 USDT
- Aggressive: 100+ USDT

⚠️ **Start kecil, scale gradually**

### Take Profit & Stop Loss
```python
TP_PCT = 0.02    # Take Profit 2% (0.02 = 2%)
SL_PCT = 0.015   # Stop Loss 1.5% (0.015 = 1.5%)
```

**Risk/Reward Ratio:**
- Current: 2% / 1.5% = **1.33** (kurang ideal)
- Better: 2% / 1% = **2.0** (standard)
- Conservative: 1% / 1% = **1.0** (break-even)
- Aggressive: 3% / 1% = **3.0** (high reward)

**Change Example:**
```python
# For 1:2 risk/reward
TP_PCT = 0.02   # +2%
SL_PCT = 0.01   # -1%
# Ratio: 2.0
```

---

## 🎯 Signal Parameters

### Bollinger Band Width Threshold
```python
BAND_SIDEWAYS = 0.02  # 2% threshold untuk sideways detection
```

**Interpretation:**
- `band < 0.02` → Sideways mode (consolidation)
- `band > 0.02` → Trending mode (breakout)

**Adjustment:**
- Lebih sensitive (ranging sering): 0.015
- Kurang sensitive (ranging jarang): 0.025

### Minimum Signal Score
```python
MIN_SCORE = 60  # Score 0-100 untuk entry
```

**Score Levels:**
- 60-69: C grade (SKIP dengan MIN_SCORE=60)
- 70-79: B grade (masuk)
- 80+: A grade (high quality signal)

**Adjustment:**
- Untuk freq tinggi: MIN_SCORE = 50
- Untuk quality tinggi: MIN_SCORE = 70-80

### Cooldown Timer
```python
COOLDOWN = 900  # 900 detik = 15 menit = 1 candle 15m
```

**Logic:** Anti double-entry dalam 1 candle

**Adjustment:**
- TF 5m: COOLDOWN = 300 (5m)
- TF 1h: COOLDOWN = 3600 (1h)

**Formula:** COOLDOWN = TF dalam detik

---

## 📈 Signal Logic

### SIDEWAYS Mode Strategy
```python
# BUY: Bottom reversal
if close < lower_bb and close > open and rsi < 40:
    # Price di bawah lower band + bullish candle + oversold RSI
    
# SELL: Top reversal  
if close > upper_bb and close < open and rsi > 60:
    # Price di atas upper band + bearish candle + overbought RSI
```

**Cocok untuk:** Range-bound, consolidation phases

### TRENDING Mode Strategy
```python
# BUY: Uptrend breakout
if close > upper_bb and close > ma and close > open:
    # Price tembus upper band + above moving average + bullish

# SELL: Downtrend breakdown
if close < lower_bb and close < ma and close < open:
    # Price tembus lower band + below moving average + bearish
```

**Cocok untuk:** Trending phases, momentum trading

---

## 🔢 Score System

Max score: **100 points**

### Component Breakdown

| Komponen | Poin | Kondisi |
|----------|------|---------|
| MA Alignment | 25 | BUY: price > MA, SELL: price < MA |
| Band Width | 25 | width > BAND_SIDEWAYS threshold |
| Volume | 25 | volume > 1.2× volume MA |
| RSI | 25 | BUY: RSI<55, SELL: RSI>45 |
| **TOTAL** | **100** | Min 60 untuk entry |

### Contoh Score Calculation
```
Signal: BUY
Close: 0.45 > MA: 0.43 ✓ (+25)
Band width: 0.025 > 0.02 ✓ (+25)
Volume: 500K > 400K×1.2=480K ✓ (+25)
RSI: 35 < 55 ✓ (+25)
---
TOTAL SCORE: 100 (A Grade) ✅ ENTRY
```

---

## 🎓 Strategy Presets

### Preset 1: Conservative (Safer)
```python
SYMBOL = "BTCUSDT"
TIMEFRAME = "1h"
USDT_SIZE = 10
TP_PCT = 0.01
SL_PCT = 0.01
MIN_SCORE = 75
BAND_SIDEWAYS = 0.015
```

**Karakteristik:**
- Sinyal lebih jarang
- Akurasi lebih tinggi
- Return stabil

### Preset 2: Aggressive (Higher Return)
```python
SYMBOL = "CLUSDT"
TIMEFRAME = "5m"
USDT_SIZE = 50
TP_PCT = 0.03
SL_PCT = 0.02
MIN_SCORE = 50
BAND_SIDEWAYS = 0.025
```

**Karakteristik:**
- Sinyal sering
- Volatility lebih tinggi
- Potential return lebih besar

### Preset 3: Balanced (Default - Recommended)
```python
SYMBOL = "CLUSDT"
TIMEFRAME = "15m"
USDT_SIZE = 25
TP_PCT = 0.02
SL_PCT = 0.015
MIN_SCORE = 60
BAND_SIDEWAYS = 0.02
```

**Karakteristik:**
- Balanced risk/reward
- Sinyal reasonable
- Good for learning

---

## 📝 Tuning Guide

### If Too Few Signals
**Problem:** Bot jarang entry

**Solutions:**
```python
# Option 1: Lower threshold
MIN_SCORE = 50  # dari 60

# Option 2: Adjust band sensitivity
BAND_SIDEWAYS = 0.025  # dari 0.02 (less sensitive)

# Option 3: Faster timeframe
TIMEFRAME = "5m"  # dari 15m

# Option 4: Longer TP
TP_PCT = 0.03  # dari 0.02 (easier to hit)
```

### If Too Many Signals (Too Risky)
**Problem:** Bot entry terlalu banyak, boros fee

**Solutions:**
```python
# Option 1: Raise threshold
MIN_SCORE = 70  # dari 60

# Option 2: Adjust band sensitivity
BAND_SIDEWAYS = 0.015  # dari 0.02 (more sensitive)

# Option 3: Reduce size
USDT_SIZE = 10  # dari 25

# Option 4: Increase SL
SL_PCT = 0.02  # dari 0.015 (less hits)
```

### If Win Rate Low (<50%)
**Problem:** Kalah lebih sering dari menang

**Solutions:**
```python
# Option 1: Better TP/SL ratio
TP_PCT = 0.03  # easier to hit
SL_PCT = 0.01  # tight stop

# Option 2: Change pair (less volatile)
SYMBOL = "BTCUSDT"  # less risky than altcoin

# Option 3: Longer timeframe
TIMEFRAME = "1h"  # from 15m (less noise)

# Option 4: Adjust RSI levels
# Di code: change rsi < 40 ke < 35 (more oversold)
```

---

## 🧪 Testing Before Live

### 1. Paper Trade (Recommended)
```bash
# Use Binance testnet account:
# https://testnet.binancefuture.com

# Change bot to use testnet:
# client = Client(API_KEY, API_SECRET, testnet=True)
```

### 2. Backtest Locally
```python
# Download historical data dari Binance
# Plot indicators (Bollinger, RSI) manual
# Check jika signal nyata di historical data
```

### 3. Small Size Live Test
```python
USDT_SIZE = 1  # Very small
MIN_SCORE = 80  # High quality only
# Monitor 24 hours
```

### 4. Scale Up Gradually
```python
Day 1-3: 1 USDT
Day 4-7: 5 USDT
Week 2: 10 USDT
Week 3: 25 USDT (normal size)
```

---

## 📊 Monitoring Metrics

Track setiap hari:

```
Win Rate = Wins / Total Trades
Example: 7 wins / 10 trades = 70% ✅

Profit Factor = Gross Profit / Gross Loss
Example: +100 / -50 = 2.0 ✅ (above 1.5 is good)

Average Trade = Total P&L / Total Trades
Example: +50 USDT / 10 trades = +5 USDT per trade

Risk/Reward Ratio = Avg Win / Avg Loss
Example: +10 / -5 = 2.0 ✅

Fee Impact = Maker 0.02% × 2 trades per order
Example: 1000 × 0.02% × 2 = 0.4 USDT fee
```

---

## 🚨 Final Checklist

Sebelum run bot:

- [ ] Test di paper trading 48+ hours
- [ ] Verify win rate > 50%
- [ ] Verify profit factor > 1.5
- [ ] Verify risk per trade = USDT_SIZE / account × 2%
- [ ] Set USDT_SIZE conservative first
- [ ] Monitor logs daily
- [ ] Have stop-loss strategy jika bot error
- [ ] Keep API key restricted to IP

---

**DYOR & Trade Safe!** 🚀
