@echo off
echo Starting Kangaroo Parallel Search (10 Workers)...
cd /d "%~dp0search_engine"
py kangaroo_search.py
pause
