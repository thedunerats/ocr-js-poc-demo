# Quick Start Script
Write-Host "🚀 Starting OCR Demo - Server and Client" -ForegroundColor Cyan
Write-Host ""

# Start server in background
Write-Host "📡 Starting Flask server on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Git Repos\ocr-js-poc-demo\server'; python run.py"

# Wait a bit for server to start
Start-Sleep -Seconds 3

# Start client
Write-Host "🎨 Starting React client on http://localhost:5173..." -ForegroundColor Yellow
Set-Location "c:\Git Repos\ocr-js-poc-demo\client"
npm run dev
