# Verify Kubernetes Deployment Status

Write-Host "🔍 checking Kubernetes Cluster Status..." -ForegroundColor Cyan

# 1. Check Minikube Status
Write-Host "`n[1] Cluster Status (Minikube):" -ForegroundColor Yellow
minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Error "Minikube is NOT running. Try restarting your terminal."
    exit 1
}

# 2. Check Pods (Your Apps)
Write-Host "`n[2] Checking Application Pods:" -ForegroundColor Yellow
minikube kubectl -- get pods
Write-Host "👉 Look for 'STATUS: Running' and 'READY: 1/1'" -ForegroundColor Gray

# 3. Check Services (URLs)
Write-Host "`n[3] Checking Services (URLs):" -ForegroundColor Yellow
minikube service list

Write-Host "`n--------------------------------------------------"
Write-Host "✅ If you see 'Running' above, your app is LIVE!" -ForegroundColor Green
Write-Host "--------------------------------------------------"
