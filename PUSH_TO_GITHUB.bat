@echo off
echo ====================================================
echo 🚀 Push to GitHub - Kangaroo Parallel Vercel
echo ====================================================
echo.
echo ⚠️  IMPORTANT: Create the GitHub repository FIRST!
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: kangaroo-parallel-vercel
echo 3. Click: Create repository
echo.
echo Press any key AFTER creating the repository...
pause >nul
echo.
echo ====================================================
echo 🔄 Pushing to GitHub...
echo ====================================================
echo.

git remote add origin https://github.com/Maslan501/kangaroo-parallel-vercel.git
if errorlevel 1 (
    echo ⚠️  Remote already exists, using existing remote
    git remote set-url origin https://github.com/Maslan501/kangaroo-parallel-vercel.git
)

echo.
echo Setting branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed! Common issues:
    echo    - Repository doesn't exist on GitHub
    echo    - Authentication failed (use Personal Access Token)
    echo    - Network connection issue
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo ✅ Successfully pushed to GitHub!
echo ====================================================
echo.
echo Your repository is now available at:
echo https://github.com/Maslan501/kangaroo-parallel-vercel
echo.
echo Next steps:
echo  - View on GitHub: https://github.com/Maslan501/kangaroo-parallel-vercel
echo  - Deploy to Vercel: vercel --prod
echo  - Clone elsewhere: git clone https://github.com/Maslan501/kangaroo-parallel-vercel.git
echo.
pause
