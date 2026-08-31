#!/usr/bin/env bash
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  python3 app.py
elif command -v python >/dev/null 2>&1; then
  python app.py
else
  echo "Python 3.10+ is required."
  exit 1
fi
