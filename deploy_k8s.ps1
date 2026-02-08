# Deploy to Minikube Script
# Phase 4: Local Kubernetes Deployment

Write-Host ">>> Starting Phase 4 Deployment..." -ForegroundColor Green

# 0. Refresh Environment Variables (in case recently installed)
try {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "[*] Refreshed Environment Variables."
} catch {
    Write-Warning "Could not refresh environment variables. You might need to restart your terminal."
}

# 1. Check Prereqs & PATH Fix
$minikubePath = Get-Command "minikube" -ErrorAction SilentlyContinue
if ($minikubePath -eq $null) {
    # Try standard paths
    $possiblePaths = @(
        "C:\Program Files\Kubernetes\Minikube\minikube.exe",
        "$env:ProgramFiles\Kubernetes\Minikube\minikube.exe"
    )
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            Write-Host "[*] Found Minikube at: $path"
            $env:Path += ";$(Split-Path $path)"
            break
        }
    }
}

if ((Get-Command "minikube" -ErrorAction SilentlyContinue) -eq $null) {
    Write-Warning "Minikube command still not found in PATH."
    Write-Warning "Please restart your computer or terminal."
    # Attempt to continue anyway, it might work if alias was set just now
}

if ((Get-Command "helm" -ErrorAction SilentlyContinue) -eq $null) {
    Write-Error "Helm is not installed. Please install it first."
    exit 1
}

# 2. Start Minikube
$minikubeStatus = minikube status --format='{{.Host}}'
if ($minikubeStatus -ne "Running") {
    Write-Host "[*] Starting Minikube..."
    minikube start --driver=docker
} else {
    Write-Host "[OK] Minikube is already running."
}

# 3. Configure Docker to use Minikube's environment
Write-Host "[*] Configuring Docker environment..."
minikube docker-env | Invoke-Expression

# 4. Build Images
Write-Host "[*] Building Backend Image (todo-backend)..."
docker build -t todo-backend:latest -f backend/Dockerfile .

Write-Host "[*] Building Frontend Image (todo-frontend)..."
docker build -t todo-frontend:latest -f frontend/Dockerfile .

# 5. Configuration
$geminiKey = $null
if (Test-Path ".env") {
    Write-Host "[*] Reading configuration from .env file..."
    foreach ($line in Get-Content ".env") {
        if ($line -match "^GEMINI_API_KEY=(.*)") {
            $geminiKey = $matches[1].Trim('"').Trim("'")
            Write-Host "[OK] Found Gemini API Key in .env"
            break
        }
    }
}

if ([string]::IsNullOrWhiteSpace($geminiKey)) {
    $geminiKey = Read-Host "Please enter your Gemini API Key"
}

# 6. Deploy Backend
Write-Host "[*] Deploying Backend..."
helm upgrade --install todo-backend ./k8s/helm/backend `
    --set env.geminiApiKey="$geminiKey"

# 7. Deploy Frontend
Write-Host "[*] Deploying Frontend..."
# Get Minikube IP
$minikubeIp = minikube ip

helm upgrade --install todo-frontend ./k8s/helm/frontend `
    --set env.nextPublicApiUrl="http://localhost:8000"

Write-Host "[OK] Deployment Complete!"
Write-Host "--------------------------------------------------"
Write-Host "[*] To access the application:"
Write-Host "1. Frontend: http://localhost:30080"
Write-Host "2. Backend:  Run 'kubectl port-forward svc/todo-backend 8000:8000'"
Write-Host "--------------------------------------------------"
Write-Host "[*] To use AI Ops:"
Write-Host "   kubectl-ai 'Scale frontend to 3 replicas'"
Write-Host "--------------------------------------------------"
