# ⚡ QUICK START - 5 Menit Setup

## 🎯 Tujuan
Bot trading otomatis berjalan di GitHub (cloud) tanpa perlu server pribadi.

---

## 📋 Checklist Pre-Setup

- [ ] Punya GitHub account
- [ ] Punya Binance Futures account (verified)
- [ ] Punya Telegram account
- [ ] Punya balance di Binance (untuk trading)

---

## 🚀 Step 1: Persiapan Credentials (15 menit)

### A. Binance API (5 min)
1. Login Binance → Account → API Management
2. Create API → Label: `TradingBot`
3. Enable: Futures Trading
4. Copy API Key & Secret
5. **RECOMMENDED:** Restrict IP address

### B. Telegram (5 min)
1. Chat @BotFather → `/newbot`
2. Follow instruksi → copy token
3. Chat bot mu, send `/start`
4. Chat @userinfobot → copy chat ID Anda

### C. Save credentials (5 min)
Simpan di notepad sementara:
```
BINANCE_API_KEY = abc123...
BINANCE_API_SECRET = xyz789...
TELEGRAM_BOT_TOKEN = 123456789:ABC...
TELEGRAM_CHAT_ID = 987654321
```

---

## 🔧 Step 2: GitHub Setup (10 menit)

### A. Create Repo
1. GitHub → Create new repository
2. Name: `trading-bot` (atau nama apapun)
3. Description: "Auto trading bot v1.0"
4. **Public** atau **Private** (both OK)
5. Click **Create repository**

### B. Add 7 Files ke Repository

Download 7 files dari output:
- `deploy-bot.yml` → rename jadi `.github/workflows/deploy-bot.yml` (create folder `.github/workflows/` dulu)
- `bot_auto_mode_v1.py`
- `requirements.txt`
- `README.md`
- `SECRETS_SETUP.md`
- `.gitignore`
- `setup.sh`

Upload semua ke repo root (except deploy-bot.yml yang masuk folder)

### C. Add GitHub Secrets (3 menit)

1. GitHub repo → Settings → Secrets and variables → Actions
2. Click **New repository secret** × 4:

| Secret Name | Paste dari Notepad |
|---|---|
| `BINANCE_API_KEY` | API key Binance |
| `BINANCE_API_SECRET` | Secret Binance |
| `TELEGRAM_BOT_TOKEN` | Token dari @BotFather |
| `TELEGRAM_CHAT_ID` | ID dari @userinfobot |

3. Save setiap secret

---

## ▶️ Step 3: Run Bot (2 menit)

### A. Manual Start (First Time)
1. Go to GitHub repo → **Actions** tab
2. Left sidebar → **"Auto Install & Run BOT v1.0"**
3. Click **"Run workflow"** → **"Run workflow"** button

### B. Check Logs
1. Workflow sedang jalan, tunggu 1-2 menit
2. Click workflow run → lihat real-time logs
3. Tunggu sampai workflow complete (✅ green)

### C. Verify Bot Running
- [ ] Telegram dapat startup message
- [ ] Telegram dapat status update setiap 5 menit
- [ ] Log di Actions tab menunjukkan bot scanning...

---

## 🎉 Done!

**Bot sekarang berjalan 24/7 di GitHub!**

### Auto Features:
- ✅ Bot jalankan otomatis setiap hari jam 00:00 UTC
- ✅ Bot restart otomatis setiap 23 jam
- ✅ Bisa trigger manual dari Actions tab
- ✅ Telegram notif real-time

---

## ⚙️ Customize Bot (Optional)

Edit `bot_auto_mode_v1.py`:

```python
SYMBOL = "BTCUSDT"  # Ganti pair
TIMEFRAME = "15m"   # Ganti timeframe
USDT_SIZE = 25      # Ganti size per trade
TP_PCT = 0.02       # Take profit 2%
SL_PCT = 0.015      # Stop loss 1.5%
MIN_SCORE = 60      # Min signal score
```

Push ke GitHub → bot otomatis update!

---

## 🛑 Stop Bot

Jika ingin stop:
1. Disable workflow di Actions tab
2. Atau delete `.github/workflows/deploy-bot.yml`

Posisi open akan tetap ada (close manual dari Binance)

---

## 📊 Monitor Bot

Check setiap hari:
1. GitHub Actions → see recent runs ✅/❌
2. Telegram → read status updates
3. Binance → verify trade history

---

## ❓ Troubleshoot

### "Workflow failed"
→ Check logs di Actions, baca error message  
→ Common: wrong secret name, missing files

### "Telegram tidak kirim notif"
→ Verify token & chat ID di SECRETS_SETUP.md  
→ Make sure bot sudah di-start (@BotFather)

### "Binance error: invalid key"
→ Verify API key & secret exact (no extra spaces)  
→ Make sure futures trading enabled

### "Bot tidak entry signal"
→ Normal! Signal jarang. Monitor 24-48 jam  
→ Check MIN_SCORE bukan terlalu tinggi

---

## 📚 More Info

- Detailed setup → buka `SECRETS_SETUP.md`
- Full documentation → buka `README.md`
- Signal logic → lihat comments di `bot_auto_mode_v1.py`

---

## 🚀 DONE!

Enjoy automated trading! Remember: **DYOR & start small** 💰

Questions? Check README.md atau SECRETS_SETUP.md
