# PowerShell launcher for Kangaroo Parallel Search
Write-Host "Starting Kangaroo Parallel Search (10 Workers)..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot\search_engine"
py kangaroo_search.py
