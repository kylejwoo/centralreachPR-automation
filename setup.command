#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Installing Playwright Chromium..."
python3 -m playwright install chromium

echo
echo "Setup complete."
echo "Run ./start.command or: source .venv/bin/activate && python3 main.py"
read -r -p "Press ENTER to close..."
