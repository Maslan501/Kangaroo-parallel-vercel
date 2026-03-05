@echo off
echo Starting Dashboard on http://localhost:5001...
cd /d "%~dp0api"
set FLASK_APP=index.py
py -m flask run --host=0.0.0.0 --port=5001
pause
