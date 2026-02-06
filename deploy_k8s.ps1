# Deploy to Minikube Script
# Phase 4: Local Kubernetes Deployment

Write-Host "🚀 Starting Phase 4 Deployment..." -ForegroundColor Green

# 1. Check Prereqs
if ((Get-Command "minikube" -ErrorAction SilentlyContinue) -eq $null) {
    Write-Error "Minikube is not installed. Please install it first."
    exit 1
}

if ((Get-Command "helm" -ErrorAction SilentlyContinue) -eq $null) {
    Write-Error "Helm is not installed. Please install it first."
    exit 1
}

# 2. Start Minikube
$minikubeStatus = minikube status --format='{{.Host}}'
if ($minikubeStatus -ne "Running") {
    Write-Host "🔧 Starting Minikube..."
    minikube start --driver=docker
} else {
    Write-Host "✅ Minikube is already running."
}

# 3. Configure Docker to use Minikube's environment
Write-Host "🐳 Configuring Docker environment..."
minikube docker-env | Invoke-Expression

# 4. Build Images
Write-Host "🔨 Building Backend Image (todo-backend)..."
docker build -t todo-backend:latest -f backend/Dockerfile .

Write-Host "🔨 Building Frontend Image (todo-frontend)..."
docker build -t todo-frontend:latest -f frontend/Dockerfile .

# 5. Configuration
$geminiKey = Read-Host "🔑 Please enter your Gemini API Key"

# 6. Deploy Backend
Write-Host "🚢 Deploying Backend..."
helm upgrade --install todo-backend ./k8s/helm/backend `
    --set env.geminiApiKey="$geminiKey"

# 7. Deploy Frontend
Write-Host "🚢 Deploying Frontend..."
# Get Minikube IP
$minikubeIp = minikube ip
$backendUrl = "http://$minikubeIp:30008" # Backend NodePort (we used ClusterIP 8000, let's expose it)
# Actually, for local dev, we might want to port-forward or use NodePort for backend too to make it accessible to browser
# Let's use kubectl port-forward for backend access by browser, or update backend to NodePort.
# Updating Backend to use NodePort 30008 to match this script logic.

helm upgrade --install todo-frontend ./k8s/helm/frontend `
    --set env.nextPublicApiUrl="http://localhost:8000" # Using manual port-forward later

Write-Host "✅ Deployment Complete!"
Write-Host "--------------------------------------------------"
Write-Host "🌍 To access the application:"
Write-Host "1. Frontend: http://localhost:30080 (via minikube tunnel or NodePort)"
Write-Host "2. Backend:  Run 'kubectl port-forward svc/todo-backend 8000:8000'"
Write-Host "--------------------------------------------------"
Write-Host "🤖 To use AI Ops:"
Write-Host "   kubectl-ai 'Scale frontend to 3 replicas'"
Write-Host "--------------------------------------------------"
