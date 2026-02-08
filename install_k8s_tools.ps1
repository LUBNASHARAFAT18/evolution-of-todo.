# Install Kubernetes Tools (Minikube, Helm, Kubectl)
# Using Winget

Write-Host "[*] Installing Kubernetes Prerequisites..." -ForegroundColor Cyan

# 1. Install Minikube
Write-Host "[1] Installing Minikube..."
winget install Kubernetes.Minikube --accept-source-agreements --accept-package-agreements --silent
if ($LASTEXITCODE -eq 0) { Write-Host "Minikube installed." -ForegroundColor Green }

# 2. Install Helm
Write-Host "[2] Installing Helm..."
winget install Helm.Helm --accept-source-agreements --accept-package-agreements --silent
if ($LASTEXITCODE -eq 0) { Write-Host "Helm installed." -ForegroundColor Green }

# 3. Install Kubectl
Write-Host "[3] Installing Kubectl..."
winget install Kubernetes.kubectl --accept-source-agreements --accept-package-agreements --silent
if ($LASTEXITCODE -eq 0) { Write-Host "Kubectl installed." -ForegroundColor Green }

Write-Host "--------------------------------------------------"
Write-Host "[*] Installation Complete!" -ForegroundColor Cyan
Write-Host "[!] PLEASE RESTART YOUR TERMINAL/POWERSHELL TO UPDATE PATH." -ForegroundColor Yellow
Write-Host ">>> Then run: .\deploy_k8s.ps1" -ForegroundColor Yellow
Write-Host "--------------------------------------------------"
