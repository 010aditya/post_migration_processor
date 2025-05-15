#!/bin/bash
echo "🔧 Initializing Migration Assist environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "✅ Environment setup complete."
