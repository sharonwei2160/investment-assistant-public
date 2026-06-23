#!/bin/bash

set -e

PRIVATE_REPO_DIR="$HOME/Git/stock-alert-system"
PUBLIC_REPO_DIR="$HOME/Git/investment-assistant-public"
PUBLIC_REPO_URL="https://github.com/sharonwei2160/investment-assistant-public.git"

echo "🚀 Start publishing public portfolio version..."

rm -rf "$PUBLIC_REPO_DIR"

git clone "$PUBLIC_REPO_URL" "$PUBLIC_REPO_DIR"

rsync -av \
  --exclude ".git" \
  --exclude ".env" \
  --exclude ".venv" \
  --exclude "__pycache__" \
  --exclude "lambda_package" \
  --exclude "lambda_deploy.zip" \
  --exclude "data/" \
  --exclude "logs/" \
  "$PRIVATE_REPO_DIR/" "$PUBLIC_REPO_DIR/"

cd "$PUBLIC_REPO_DIR"

# Remove sensitive files if they exist
rm -f .env
rm -f app/watchlist.json
rm -f portfolio.xlsx
rm -f *.xlsx

# Use sample files for public repo
if [ -f app/watchlist_sample.json ]; then
  cp app/watchlist_sample.json app/watchlist.json
fi

git add .
git commit -m "Update public portfolio version" || echo "No changes to commit"
git push origin main

echo "✅ Public repository updated successfully."
