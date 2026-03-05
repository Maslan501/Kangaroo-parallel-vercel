@echo off
echo ====================================================
echo 🔍 Testing Kangaroo Parallel Installation
echo ====================================================
echo.

echo [1/5] Checking Python installation...
py --version
if errorlevel 1 (
    echo ❌ Python not found! Install Python 3.12+
    pause
    exit /b 1
)
echo ✅ Python found
echo.

echo [2/5] Checking directory structure...
if not exist "api\index.py" (
    echo ❌ API files missing!
    pause
    exit /b 1
)
if not exist "search_engine\kangaroo_search.py" (
    echo ❌ Search engine missing!
    pause
    exit /b 1
)
if not exist "api\templates\dashboard.html" (
    echo ❌ Dashboard template missing!
    pause
    exit /b 1
)
echo ✅ All directories OK
echo.

echo [3/5] Checking dependencies...
py -c "import flask" 2>nul
if errorlevel 1 (
    echo ⚠️  Flask not installed
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo ✅ Flask installed
)
echo.

echo [4/5] Testing work_files directory...
if not exist "work_files" mkdir work_files
echo ✅ Work files directory ready
echo.

echo [5/5] Checking launcher scripts...
if not exist "START_ALL.bat" (
    echo ❌ Launcher scripts missing!
    pause
    exit /b 1
)
echo ✅ Launcher scripts found
echo.

echo ====================================================
echo ✅ Installation test PASSED!
echo ====================================================
echo.
echo You can now run: START_ALL.bat
echo.
echo Or manually:
echo   start_parallel_search.bat  - Start 10 workers
echo   start_dashboard.bat        - Start dashboard
echo.
pause
