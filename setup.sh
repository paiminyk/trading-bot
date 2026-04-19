#!/bin/bash

# ===============================================
# AUTO SETUP SCRIPT untuk Trading Bot
# ===============================================

echo "🚀 AUTO MODE BOT v1.0 - GitHub Setup"
echo "======================================"
echo ""

# Check if git installed
if ! command -v git &> /dev/null; then
    echo "❌ Git tidak terinstall. Install git dulu:"
    echo "   Ubuntu: sudo apt-get install git"
    echo "   Mac: brew install git"
    exit 1
fi

echo "✅ Git terinstall"
echo ""

# 1. Ask for GitHub username
read -p "📌 GitHub Username: " GITHUB_USER
read -p "📌 Repository Name: " REPO_NAME

echo ""
echo "Creating directories..."

# 2. Create .github/workflows directory
mkdir -p .github/workflows
mkdir -p .github/scripts

echo "✅ Created directories"
echo ""

# 3. Copy files
echo "Copying bot files..."

# Check if files exist di current directory
if [ ! -f "bot_auto_mode_v1.py" ]; then
    echo "⚠️ Warning: bot_auto_mode_v1.py not found"
    echo "Please ensure bot_auto_mode_v1.py is in current directory"
fi

if [ ! -f "requirements.txt" ]; then
    echo "⚠️ Warning: requirements.txt not found"
fi

if [ ! -f "deploy-bot.yml" ]; then
    echo "⚠️ Warning: deploy-bot.yml not found in current directory"
    echo "Creating deploy-bot.yml..."
    
    # Create the workflow file
    cat > .github/workflows/deploy-bot.yml << 'EOF'
name: Auto Install & Run BOT v1.0

on:
  push:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Create environment file
        run: |
          cat > config.env << EOF
          API_KEY=${{ secrets.BINANCE_API_KEY }}
          API_SECRET=${{ secrets.BINANCE_API_SECRET }}
          BOT_TOKEN=${{ secrets.TELEGRAM_BOT_TOKEN }}
          CHAT_ID=${{ secrets.TELEGRAM_CHAT_ID }}
          EOF
          chmod 600 config.env

      - name: Run Trading Bot
        run: |
          timeout 82800 python bot_auto_mode_v1.py
        env:
          PYTHONUNBUFFERED: 1
EOF
    echo "✅ Created deploy-bot.yml"
fi

echo ""
echo "======================================"
echo "📋 NEXT STEPS:"
echo "======================================"
echo ""
echo "1️⃣  Initialize Git & Push to GitHub:"
echo ""
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Add: Auto Mode Bot v1.0'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "2️⃣  Add GitHub Secrets (Settings → Secrets):"
echo ""
echo "   • BINANCE_API_KEY = your API key"
echo "   • BINANCE_API_SECRET = your API secret"
echo "   • TELEGRAM_BOT_TOKEN = your bot token"
echo "   • TELEGRAM_CHAT_ID = your chat ID"
echo ""
echo "3️⃣  Verify Files:"
echo ""
echo "   ✓ .github/workflows/deploy-bot.yml"
echo "   ✓ bot_auto_mode_v1.py"
echo "   ✓ requirements.txt"
echo "   ✓ README.md"
echo ""
echo "4️⃣  Go to Actions tab & Run manually first"
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
