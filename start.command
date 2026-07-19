#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Virtual environment not found."
  echo "Run ./setup.command first."
  read -r -p "Press ENTER to close..."
  exit 1
fi

source .venv/bin/activate
python3 main.py
