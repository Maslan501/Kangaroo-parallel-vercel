@echo off
echo ====================================================
echo Kangaroo Parallel Search + Dashboard System
echo ====================================================
echo.
echo Starting 10 Parallel Workers...
start "Kangaroo Search" "%~dp0start_parallel_search.bat"
timeout /t 2 /nobreak >nul
echo.
echo Starting Dashboard at http://localhost:5001...
start "Dashboard" "%~dp0start_dashboard.bat"
echo.
echo ====================================================
echo Both systems are starting in separate windows!
echo Dashboard: http://localhost:5001
echo ====================================================
pause
