# 🤖 Auto Mode Trading Bot v1.0 - GitHub Auto Deploy

Bot trading otomatis untuk Binance Futures dengan deployment langsung melalui GitHub Actions.

## 📋 Fitur Utama

- ✅ **Auto Deploy via GitHub Actions** - Bot berjalan otomatis di cloud
- 📊 **Signal Based** - Bollinger Band + RSI + Volume confirmation
- 🎯 **Risk Management** - TP/SL otomatis + Cooldown anti-double entry
- 📱 **Telegram Notifications** - Live alerts setiap trade
- 🔄 **Auto Restart** - Bot restart otomatis setiap 23 jam
- 💰 **Position Tracking** - Cek posisi aktif sebelum entry

---

## 🚀 Setup 1-2-3 (GitHub)

### 1️⃣ Fork atau Clone Repository

```bash
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
```

### 2️⃣ Buat GitHub Secrets (untuk Binance API & Telegram)

Di GitHub repo Anda:
1. Settings → Secrets and variables → Actions
2. Tambahkan 4 secrets ini:

| Secret Name | Nilai | Contoh |
|-------------|-------|--------|
| `BINANCE_API_KEY` | API Key dari Binance Futures | `abc123def456...` |
| `BINANCE_API_SECRET` | Secret dari Binance Futures | `xyz789uvw...` |
| `TELEGRAM_BOT_TOKEN` | Bot token dari BotFather | `123456789:ABCdefghijkl...` |
| `TELEGRAM_CHAT_ID` | Chat ID mu di Telegram | `987654321` |

#### 📍 Cara dapat Binance API:
1. Login ke Binance → Account → API Management
2. Create API → Copy API Key & Secret
3. Enable Futures Trading di API settings
4. Recommend: Restrict to IP address

#### 📍 Cara dapat Telegram Bot Token & Chat ID:
```
1. Chat @BotFather → /newbot → ikuti instruksi → copy token
2. Chat @userinfobot → lihat chat ID mu
```

### 3️⃣ Push Files ke Repository

```bash
# Copy 3 file ini ke folder root repo:
# - bot_auto_mode_v1.py
# - .github/workflows/deploy-bot.yml
# - requirements.txt

git add .
git commit -m "Add: Auto Mode Bot v1.0 with GitHub Actions"
git push origin main
```

---

## 📁 File Structure

```
your-repo/
├── bot_auto_mode_v1.py           # Main bot script
├── requirements.txt              # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy-bot.yml        # GitHub Actions workflow
└── README.md                      # Documentation
```

---

## ⚙️ Konfigurasi Bot

Edit file `bot_auto_mode_v1.py` untuk customize:

```python
# Trading Parameters
SYMBOL    = "CLUSDT"        # Pair yang dimainkan
TIMEFRAME = "15m"           # Timeframe candle
USDT_SIZE = 25              # Size per trade (USDT)

# Risk Management
TP_PCT = 0.02               # Take Profit 2%
SL_PCT = 0.015              # Stop Loss 1.5%
TP_RATIO = 1.33             # Risk/Reward ratio

# Signal Parameters
MIN_SCORE = 60              # Minimum score untuk entry
BAND_SIDEWAYS = 0.02        # Bollinger Band width threshold
COOLDOWN = 900              # Cooldown antar trade (900s = 15m)
```

---

## 🔄 Workflow GitHub Actions

Bot akan berjalan otomatis di 3 kondisi:

### 1. **Schedule (Harian)**
```yaml
schedule:
  - cron: '0 0 * * *'  # Setiap hari jam 00:00 UTC
```

### 2. **Push ke Main Branch**
Setiap kali push ke main, GitHub Actions trigger otomatis

### 3. **Manual Trigger**
Di GitHub UI:
- Actions → Auto Install & Run BOT v1.0 → Run workflow

---

## 📊 Signal Logic

### SIDEWAYS Mode (Band width < 0.02)
- **BUY**: Price < Lower BB + Bullish candle + RSI < 40
- **SELL**: Price > Upper BB + Bearish candle + RSI > 60

### TRENDING Mode (Band width > 0.02)
- **BUY**: Price > Upper BB + Close > MA + Bullish candle
- **SELL**: Price < Lower BB + Close < MA + Bearish candle

### Score System (Max 100)
```
25 pts: Direction alignment dengan MA
25 pts: Band width cukup lebar
25 pts: Volume > 1.2x average
25 pts: RSI alignment dengan signal
```

Min score 60 untuk entry ✅

---

## 📱 Telegram Notifications

Bot akan kirim notifikasi:

1. **Startup Message** - Bot mulai running
2. **Status Update** - Setiap 5 menit (pair price, signal, score)
3. **Signal Alert** - Signal detected (dengan reason)
4. **Entry Confirmation** - Trade executed (TP/SL/RR ratio)
5. **Error Alert** - Jika ada error

---

## 🛡️ Safety Features

✅ **Position Check** - Tidak entry jika ada posisi aktif  
✅ **Cooldown Timer** - 15 menit antar trade (hindari double entry)  
✅ **Candle Confirmation** - Tunggu candle close sebelum entry  
✅ **Order Cancellation** - Cancel semua pending orders sebelum entry  
✅ **Risk Management** - TP/SL otomatis + closePosition flag  

---

## 📈 Backtesting & Paper Trading

Sebelum live trading:

1. **Paper Trade** (Recommended)
   - Jalankan bot di account testnet dulu
   - Atau set `USDT_SIZE = 0.1` untuk test dengan size kecil

2. **Monitor 48-72 jam**
   - Lihat performance signal
   - Adjust MIN_SCORE jika needed
   - Fine-tune TP/SL percentage

---

## 🔧 Troubleshooting

### ❌ "API Key invalid"
- Check GitHub Secrets (exact spelling)
- Verify Binance API Key & Secret
- Make sure futures trading enabled

### ❌ "Telegram not sending"
- Verify TELEGRAM_BOT_TOKEN (copy exact dari @BotFather)
- Verify TELEGRAM_CHAT_ID (use @userinfobot)
- Check message is not empty

### ❌ "Order failed"
- Check symbol precision (qty/price format)
- Verify sufficient balance
- Check Binance order types supported

### ❌ Workflow not running
- Check .yml file in `.github/workflows/`
- Verify branch name (main vs master)
- Check syntax (YAML sensitive to indentation)

---

## 📊 Monitoring Dashboard

Check bot status di GitHub:

1. Go to Actions tab
2. Click "Auto Install & Run BOT v1.0"
3. See:
   - ✅ Workflow Status (Success/Failed)
   - ⏱️ Run Duration (23 hours per cycle)
   - 📋 Logs (real-time output)

---

## 💡 Tips & Optimization

### Untuk Profitability
- Start dengan MIN_SCORE tinggi (70-80)
- Perlahan turunkan jika signal jarang
- Monitor win rate sebelum increase leverage
- Use conservative TP/SL ratio (1:1.5 minimum)

### Untuk Stability
- Jalankan di pair liquid (CLUSDT, BTCUSDT, ETHUSDT)
- Avoid news/event times
- Set position size kecil (test phase)
- Monitor logs setiap hari

### Cost Optimization
- GitHub Actions gratis 2000 minutes/month
- 23 hours/day × 30 days = 690 hours/month ✅ dalam budget
- Binance fee: maker 0.02% per trade

---

## 🚨 Risk Warning

⚠️ **DYOR (Do Your Own Research)**

Cryptocurrency trading involves **HIGH RISK**:
- This bot is **NOT** financial advice
- Past performance ≠ future results
- Start dengan small size
- Use stop losses religiously
- Never trade with money you can't afford to lose

---

## 📝 Roadmap v2.0

- [ ] Multi-pair support
- [ ] Custom webhook alerts
- [ ] Database tracking (trade history)
- [ ] Web dashboard (Streamlit)
- [ ] Advanced ML signals
- [ ] Risk scaling (dynamic size)

---

## 📞 Support

Issues? Questions?

1. Check Troubleshooting section
2. Review bot logs in GitHub Actions
3. Test locally first:
   ```bash
   pip install -r requirements.txt
   python bot_auto_mode_v1.py
   ```

---

## 📄 License

MIT License - Use at your own risk

---

**Happy Trading! 🚀**

Last updated: 2025-04-19  
Bot Version: 1.0  
Status: Production Ready ✅
