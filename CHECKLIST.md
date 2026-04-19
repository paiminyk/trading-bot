# ✅ Complete Setup & Troubleshooting Checklist

---

## 🚀 PRE-SETUP CHECKLIST

### Accounts & Access
- [ ] GitHub account aktif
- [ ] Binance account (verified KYC)
- [ ] Binance Futures enabled
- [ ] Telegram account aktif
- [ ] USDT balance di Binance (untuk trading)

### Credentials Gathered
- [ ] Binance API Key copied
- [ ] Binance API Secret copied
- [ ] Telegram Bot Token copied (dari @BotFather)
- [ ] Telegram Chat ID copied (dari @userinfobot)

---

## 📥 SETUP PHASE CHECKLIST

### Step 1: GitHub Repository
- [ ] Repository created (public or private)
- [ ] Files uploaded ke repo root:
  - [ ] `bot_auto_mode_v1.py`
  - [ ] `requirements.txt`
  - [ ] `README.md`
  - [ ] `QUICK_START.md`
  - [ ] `CONFIG_GUIDE.md`
  - [ ] `SECRETS_SETUP.md`
  - [ ] `.gitignore`

### Step 2: Workflow File
- [ ] Folder `.github/workflows/` created
- [ ] `deploy-bot.yml` file uploaded ke `.github/workflows/deploy-bot.yml`
- [ ] File contains all 4 secret references:
  - [ ] `${{ secrets.BINANCE_API_KEY }}`
  - [ ] `${{ secrets.BINANCE_API_SECRET }}`
  - [ ] `${{ secrets.TELEGRAM_BOT_TOKEN }}`
  - [ ] `${{ secrets.TELEGRAM_CHAT_ID }}`

### Step 3: GitHub Secrets
- [ ] Settings → Secrets and variables → Actions opened
- [ ] 4 secrets created dengan EXACT spelling:
  - [ ] `BINANCE_API_KEY` = [paste exact dari Binance]
  - [ ] `BINANCE_API_SECRET` = [paste exact dari Binance]
  - [ ] `TELEGRAM_BOT_TOKEN` = [paste exact token]
  - [ ] `TELEGRAM_CHAT_ID` = [paste exact chat ID]
- [ ] No extra spaces di secrets
- [ ] Secrets visible di Actions tab

### Step 4: Git Commit (Optional but Recommended)
```bash
git add .
git commit -m "Add: Auto Mode Bot v1.0"
git push origin main
```
- [ ] All files committed
- [ ] No API keys visible di repo (check .gitignore)

---

## ▶️ FIRST RUN CHECKLIST

### Trigger Workflow
- [ ] Go to GitHub Actions tab
- [ ] Select "Auto Install & Run BOT v1.0"
- [ ] Click "Run workflow"
- [ ] Yellow "pending" status visible
- [ ] Status changes to green "Success" dalam 2-3 minutes

### Monitor First Run
- [ ] Expand workflow run
- [ ] See logs di "Run Trading Bot" section
- [ ] Look for:
  - [ ] ✅ "Binance client initialized"
  - [ ] ✅ "Bot scanning... CLUSDT"
  - [ ] ✅ Terminal output (price, signal, score)

### Telegram Notifications
- [ ] Receive startup message
  ```
  🤖 AUTO MODE BOT v1.0 STARTED (Github Actions)
  PAIR: CLUSDT
  SIZE: $25
  ...
  ```
- [ ] Receive status update every 5 minutes
  ```
  📊 AUTO MODE BOT v1.0
  PAIR: CLUSDT
  PRICE: 0.xxxx
  SIGNAL: None/BUY/SELL
  SCORE: xx (A/B/C)
  ...
  ```

---

## 📊 MONITORING CHECKLIST (Daily)

### GitHub Actions
- [ ] Check Actions tab for recent runs
- [ ] All runs show ✅ green status
- [ ] No ❌ red failed runs
- [ ] Last run time recent (within 24h)

### Telegram
- [ ] Receiving status updates every ~5 min
- [ ] Messages format correct (no errors)
- [ ] Trading signals showing up
- [ ] Entry confirmations sent when trade executed

### Trading Performance
- [ ] Check Binance Futures position history
- [ ] Review recent trades:
  - [ ] Check TP hit rate
  - [ ] Check SL hit rate
  - [ ] Calculate win rate
  - [ ] Review profit/loss

### Logs Analysis
- [ ] Click last workflow run
- [ ] Scroll through logs
- [ ] Check for patterns:
  - [ ] Entry signals frequent enough?
  - [ ] Candles closing properly?
  - [ ] Any error messages?

---

## 🚨 TROUBLESHOOTING FLOWCHART

### ISSUE: Workflow Failed (Red ❌)

**Check logs:**
```
1. Actions tab → click failed workflow
2. Expand "Run Trading Bot" step
3. Read error message carefully
```

**Common errors:**

#### ❌ "ModuleNotFoundError: No module named 'binance'"
**Solution:**
- [ ] Check `requirements.txt` has all dependencies
- [ ] Verify file uploaded to repo root
- [ ] Re-run workflow (cache might be stale)

#### ❌ "API Key invalid / unauthorized"
**Solution:**
- [ ] Go Settings → Secrets → check secret values
- [ ] Verify EXACT copy dari Binance (no extra spaces)
- [ ] Check Binance API still active (not disabled)
- [ ] Try regenerate new API key dalam Binance
- [ ] Verify futures trading enabled di API

#### ❌ "Invalid symbol CLUSDT"
**Solution:**
- [ ] Check symbol spelling: CLUSDT (must be exactly)
- [ ] Verify pair exists di Binance Futures
- [ ] Try BTCUSDT dulu (paling liquid)

#### ❌ "Timeout waiting for response"
**Solution:**
- [ ] Network issue (usually temporary)
- [ ] Bot will retry automatically
- [ ] Check GitHub Actions internet (usually OK)

#### ❌ "YAML parsing error"
**Solution:**
- [ ] Check `.github/workflows/deploy-bot.yml` formatting
- [ ] YAML is sensitive to indentation (use 2 spaces)
- [ ] Re-copy file from output bundle
- [ ] Avoid tabs (use spaces only)

---

### ISSUE: Telegram Not Receiving Messages

#### ❌ No startup message
**Checklist:**
- [ ] Secret name: `TELEGRAM_BOT_TOKEN` (exact spelling)
- [ ] Secret value starts with digits: `123456789:ABC...`
- [ ] Secret name: `TELEGRAM_CHAT_ID` (exact spelling)
- [ ] Chat ID is numeric: `987654321`
- [ ] Bot chatted (@yourbotname) to receive updates

**Test:**
```bash
# Run locally to test:
curl "https://api.telegram.org/botYOUR_TOKEN/getMe"
# Should return: "ok":true
```

#### ❌ Status updates missing
**Checklist:**
- [ ] Check logs in GitHub Actions (bot is running)
- [ ] Wait 5+ minutes (status sent every 5 min)
- [ ] Check Telegram chat (not DM to bot)
- [ ] Verify not in mute (🔔 unmute channel)

**Reset:**
1. [ ] Delete bot & @BotFather
2. [ ] Create new bot with @BotFather
3. [ ] Update secret `TELEGRAM_BOT_TOKEN`
4. [ ] Re-run workflow

---

### ISSUE: Bot Running But No Trades

#### ❌ Signal never triggers
**Check:**
1. [ ] Logs show scores consistently low?
   - If yes: signal too stringent, lower MIN_SCORE
2. [ ] Pair CLUSDT very stable (no volatility)?
   - If yes: switch to BTCUSDT or ETHUSDT
3. [ ] Running only for 1-2 hours?
   - If yes: wait longer (signal might come next day)

**Tuning:**
```python
# Lower minimum score
MIN_SCORE = 50  # dari 60

# Wider band threshold
BAND_SIDEWAYS = 0.025  # dari 0.02

# Switch pair
SYMBOL = "BTCUSDT"  # dari CLUSDT
```

#### ❌ Signal triggers but position exists (SKIP message)
**This is normal!**
- [x] Bot correctly skips entry saat ada posisi aktif
- [ ] Check if previous trade masih open
- [ ] Close position manually atau wait untuk SL/TP hit
- [ ] Next signal akan entry

**Check:**
```
Telegram: "⚠️ Ada posisi aktif, skip entry"
= Normal behavior (anti-multiple positions)
```

#### ❌ Score too low ("SKIP ⚠️" messages)
**Problem:** MIN_SCORE threshold terlalu tinggi

**Solutions:**
```python
# Lower the threshold
MIN_SCORE = 50  # dari 60 atau 70

# Adjust components:
BAND_SIDEWAYS = 0.025  # less strict band check
TP_PCT = 0.03          # easier to hit TP
```

---

### ISSUE: Bot Consuming Too Much Resources

#### ⚠️ Workflow running too long
**GitHub Actions limit:** 6 hours per workflow run

**Current bot setup:** 23 hours timeout with auto-restart
- [ ] This is handled (bot restarts every ~23h)
- [ ] Each restart appears as new workflow run
- [ ] This is NORMAL

**Monitoring:**
- [ ] Check Actions → see multiple runs per day
- [ ] Each run lasts ~23 hours then restarts
- [ ] This uses ~690 hours/month (within free 2000h limit)

---

## 🔐 SECURITY CHECKLIST

### API Key Security
- [ ] API Key NOT hardcoded dalam Python file
- [ ] API Key in GitHub Secrets ONLY
- [ ] Binance API restricted to IP address (recommended)
- [ ] Withdrawals disabled pada Binance API
- [ ] Futures trading enabled, spot trading disabled

### Repository Security
- [ ] `.gitignore` includes `.env` & `config.env`
- [ ] No secrets visible dalam git history
- [ ] Repository (public or private, both safe)
- [ ] No other users have write access

### Telegram Security
- [ ] Bot token not shared anywhere
- [ ] Chat ID only from bot/yourself
- [ ] No recording of trades in public channels

### Binance Account
- [ ] Authenticator (2FA) enabled
- [ ] Email verified
- [ ] IP whitelist active (if available)
- [ ] Recovery codes backed up

---

## 📈 PERFORMANCE CHECKLIST (Weekly)

### Trading Metrics
- [ ] Win rate tracked (goal: >50%)
- [ ] Profit factor calculated (goal: >1.5)
- [ ] Average trade profit measured
- [ ] Risk per trade monitored (<2% per trade)

### Bot Health
- [ ] No errors dalam GitHub logs
- [ ] Telegram notifications regular
- [ ] API calls working (no timeouts)
- [ ] Binance orders executing cleanly

### Signal Quality
- [ ] Signals realistic (not too frequent)
- [ ] Score distribution analyzed
  - How many A grades? B grades? C grades?
  - Goal: mix of A & B grades, few C
- [ ] False signal rate acceptable

### Fee Impact
- [ ] Maker fee = 0.02% per trade
- [ ] 2 orders per trade (entry + exit) = 0.04% per round trip
- [ ] Track: Total fee / Total profit
  - Goal: fees < 10% of profits

---

## 🛑 EMERGENCY SHUTDOWN

### If Bot Malfunctions
1. [ ] Go to GitHub Actions
2. [ ] Click workflow → Disable workflow
3. [ ] Binance → manually close open positions
4. [ ] Cancel pending orders

### If Lost Access
1. [ ] GitHub: reset password & security
2. [ ] Binance: change API key + password
3. [ ] Telegram: secure bot (@BotFather → /revoke)

### If Suspicious Activity
1. [ ] Disable bot immediately
2. [ ] Review Binance trade history
3. [ ] Check API logs untuk unauthorized access
4. [ ] Regenerate API key
5. [ ] Update GitHub secret

---

## 📞 QUICK REFERENCE

**Files locations:**
- Bot script: `bot_auto_mode_v1.py` (repo root)
- Workflow: `.github/workflows/deploy-bot.yml`
- Config params: Edit `bot_auto_mode_v1.py` line 20-30
- Secrets: GitHub Settings → Secrets (4 items)

**Important links:**
- Binance Futures: https://www.binance.com/en/futures/CLUSDT
- GitHub Actions: https://github.com/YOUR_USER/your-repo/actions
- Telegram Chat: Find @YOUR_BOT_NAME

**Support docs:**
- Setup help: `QUICK_START.md` (5 min guide)
- Config help: `CONFIG_GUIDE.md` (parameter tuning)
- Secrets help: `SECRETS_SETUP.md` (API keys guide)
- Full docs: `README.md` (comprehensive)

---

**You're all set! Happy trading! 🚀**
