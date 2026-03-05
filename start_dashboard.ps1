# PowerShell launcher for Dashboard
Write-Host "Starting Dashboard on http://localhost:5001..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot\api"
$env:FLASK_APP = "index.py"
py -m flask run --host=0.0.0.0 --port=5001
