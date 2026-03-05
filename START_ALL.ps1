# Master launcher for both systems
Write-Host "====================================================" -ForegroundColor Green
Write-Host "Kangaroo Parallel Search + Dashboard System" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting 10 Parallel Workers..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start_parallel_search.ps1"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Starting Dashboard at http://localhost:5001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start_dashboard.ps1"

Write-Host ""
Write-Host "====================================================" -ForegroundColor Green
Write-Host "Both systems are running in separate windows!" -ForegroundColor Cyan
Write-Host "Dashboard: http://localhost:5001" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit this window (workers will continue)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
