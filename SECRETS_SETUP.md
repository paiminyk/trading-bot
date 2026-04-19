# 🔐 GitHub Secrets Setup - Panduan Lengkap

## ⚠️ SECURITY FIRST

**JANGAN PERNAH** hardcode API keys di file Python!  
**SELALU** gunakan GitHub Secrets untuk credentials.

---

## 📍 Step-by-Step Setup

### 1️⃣ Pergi ke Settings Repository

1. Buka GitHub repo Anda
2. Klik **Settings** tab (di bagian atas)
3. Di sidebar kiri, klik **Secrets and variables** → **Actions**

### 2️⃣ Tambahkan 4 Secrets

Klik **"New repository secret"** untuk setiap secret:

---

## 🔑 Secret #1: BINANCE_API_KEY

### Cara dapat dari Binance:

1. Login ke Binance.com
2. Klik avatar → Account
3. Pilih **API Management**
4. Jika belum ada, klik **Create API**
5. Label: `TradingBot` atau nama apapun
6. Copy **API Key** (kolom pertama)
7. Paste di GitHub Secret

### Contoh:
```
Key Name: BINANCE_API_KEY
Value: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz...
```

⚠️ Pastikan **futures trading enabled** di API settings!

---

## 🔑 Secret #2: BINANCE_API_SECRET

Dari Binance API Management yang sama:

1. Di bawah API Key, ada **Secret Key** (tersembunyi)
2. Klik mata icon untuk tampilkan
3. Copy **Secret Key**
4. Paste di GitHub Secret

### Contoh:
```
Key Name: BINANCE_API_SECRET
Value: xyz123abc456def789ghi012jkl345mno678pqr901stu234vwx...
```

⚠️ **JANGAN** share secret key ini ke siapa-siapa!

---

## 🔑 Secret #3: TELEGRAM_BOT_TOKEN

### Cara dapat:

1. Buka Telegram
2. Cari & chat **@BotFather**
3. Kirim command: `/newbot`
4. Follow instruksi:
   - Nama bot: `MyTradingBot` atau apapun
   - Username: `my_trading_bot_xxxxx` (harus unique)
5. BotFather akan kirim token
6. Copy token tersebut

### Contoh:
```
Key Name: TELEGRAM_BOT_TOKEN
Value: 123456789:ABCdefGHIjklmnOPQrstUVwxyzABCdEfGHij
```

⚠️ Token dimulai dengan **angka diikuti colon (:)**

---

## 🔑 Secret #4: TELEGRAM_CHAT_ID

### Cara dapat:

**Option A - Langsung dari bot:**

1. Buka bot Anda (dari BotFather)
2. Kirim `/start`
3. Pergi ke: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Ganti `<YOUR_BOT_TOKEN>` dengan token dari Secret #3
5. Cari `"from":{"id":xxxxx...` 
6. Angka tersebut adalah Chat ID Anda

**Option B - Gunakan bot helper:**

1. Chat **@userinfobot**
2. Bot akan kirim ID Anda
3. Itu adalah Chat ID

### Contoh:
```
Key Name: TELEGRAM_CHAT_ID
Value: 987654321
```

---

## ✅ Verify Secrets Sudah Benar

Di GitHub Actions workflow file (`.github/workflows/deploy-bot.yml`), bot menggunakan secrets seperti ini:

```yaml
- name: Create environment file
  run: |
    cat > config.env << EOF
    API_KEY=${{ secrets.BINANCE_API_KEY }}
    API_SECRET=${{ secrets.BINANCE_API_SECRET }}
    BOT_TOKEN=${{ secrets.TELEGRAM_BOT_TOKEN }}
    CHAT_ID=${{ secrets.TELEGRAM_CHAT_ID }}
    EOF
```

**Jika secrets benar**, maka:
- ✅ `config.env` akan dibuat dengan values yang benar
- ✅ Bot bisa login ke Binance
- ✅ Bot bisa kirim notifikasi ke Telegram

---

## 🧪 Test Credentials

Sebelum run bot, test di local:

```bash
# 1. Create .env file locally
cat > .env << EOF
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
BOT_TOKEN=your_telegram_token
CHAT_ID=your_telegram_id
EOF

# 2. Install dependencies
pip install python-binance requests python-dotenv

# 3. Test Binance connection
python -c "
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))
print('✅ Binance connected!')
print('Account balance:', client.futures_account()['totalWalletBalance'])
"

# 4. Test Telegram
python -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
url = f'https://api.telegram.org/bot{token}/sendMessage'
requests.get(url, params={'chat_id': chat_id, 'text': '✅ Bot Connected!'})
print('✅ Telegram connected!')
"
```

---

## 🚨 If Secrets Not Working

### ❌ "API Key Invalid"
- [ ] Copy exact dari Binance (no extra spaces)
- [ ] Verify futures trading enabled di API settings
- [ ] Try regenerate API key di Binance

### ❌ "Telegram not sending"
- [ ] Verify token format: `digits:LETTERS_NUMBERS`
- [ ] Verify chat ID is numeric
- [ ] Test token: `curl "https://api.telegram.org/botYOUR_TOKEN/getMe"`
- [ ] Make sure you've chatted with bot (`/start`)

### ❌ "Secret not found in workflow"
- [ ] Check spelling **EXACTLY** matches workflow file
- [ ] Secrets are case-sensitive: `BINANCE_API_KEY` ≠ `binance_api_key`
- [ ] Wait 1-2 minutes after adding secret (caching)
- [ ] Refresh page & try again

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use different API key for each app
- ✅ Restrict IP address di Binance API settings
- ✅ Disable withdrawals di API settings
- ✅ Rotate credentials monthly
- ✅ Use GitHub Secrets untuk semua sensitive data

### ❌ DON'T:
- ❌ Hardcode API keys di Python files
- ❌ Commit `.env` files
- ❌ Share secrets di Discord/Telegram/Email
- ❌ Use same API key untuk multiple bots
- ❌ Enable withdraw permission di bot API

---

## 📊 Ready to Run?

Once all 4 secrets are added:

1. Go to **Actions** tab
2. Select **"Auto Install & Run BOT v1.0"**
3. Click **"Run workflow"**
4. Check logs

Bot should start dalam 30 detik! 🚀

---

**Questions?** Re-read this guide or check bot logs di GitHub Actions.

Stay safe! 🔐
