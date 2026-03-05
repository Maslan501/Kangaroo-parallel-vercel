# Push to GitHub - PowerShell Script
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "🚀 Push to GitHub - Kangaroo Parallel Vercel" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  IMPORTANT: Create the GitHub repository FIRST!" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to: https://github.com/new"
Write-Host "2. Repository name: kangaroo-parallel-vercel"
Write-Host "3. Click: Create repository"
Write-Host ""
Write-Host "Press any key AFTER creating the repository..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "🔄 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Add remote
Write-Host "Adding remote repository..." -ForegroundColor White
git remote add origin https://github.com/Maslan501/kangaroo-parallel-vercel.git 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Remote already exists, updating URL..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/Maslan501/kangaroo-parallel-vercel.git
}

Write-Host ""
Write-Host "Setting branch to main..." -ForegroundColor White
git branch -M main

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor White
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Push failed! Common issues:" -ForegroundColor Red
    Write-Host "   - Repository doesn't exist on GitHub" -ForegroundColor Yellow
    Write-Host "   - Authentication failed (use Personal Access Token)" -ForegroundColor Yellow
    Write-Host "   - Network connection issue" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To generate a token: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host ""
    Pause
    exit 1
}

Write-Host ""
Write-Host "====================================================" -ForegroundColor Green
Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your repository is now available at:" -ForegroundColor White
Write-Host "https://github.com/Maslan501/kangaroo-parallel-vercel" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  - View on GitHub: " -NoNewline; Write-Host "https://github.com/Maslan501/kangaroo-parallel-vercel" -ForegroundColor Cyan
Write-Host "  - Deploy to Vercel: " -NoNewline; Write-Host "vercel --prod" -ForegroundColor Cyan
Write-Host "  - Clone elsewhere: " -NoNewline; Write-Host "git clone https://github.com/Maslan501/kangaroo-parallel-vercel.git" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
