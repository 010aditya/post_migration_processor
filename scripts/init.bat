@echo off
echo 🔧 Initializing Migration Assist environment...
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Environment setup complete.
