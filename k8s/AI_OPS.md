# AI-Assisted Kubernetes Operations (Phase 4)

This guide documents how to use AI agents for managing your local Kubernetes cluster.

## 1. 🔍 kubectl-ai (The Operator)

`kubectl-ai` allows you to interact with your cluster using natural language through the Gemini-powered backend.

### Setup
Ensure you have `kubectl-ai` installed (part of the tech stack reqs).

### Common Commands

**Scaling:**
```bash
kubectl-ai "Scale the todo-backend deployment to 3 replicas"
```

**Debugging:**
```bash
kubectl-ai "Why is the todo-frontend pod crashing? Show me logs and events."
```

**Inspection:**
```bash
kubectl-ai "List all pods in the default namespace and show their resource usage"
```

## 2. 🛡️ Kagent (The SRE)

`Kagent` monitors cluster health and provides proactive recommendations.

### Setup
Deploy Kagent to your cluster (using the official Helm chart or manifest).

### Capabilities
- **CrashLoopBackOff detection**: Automatically analyzes logs of crashing pods.
- **Resource Optimization**: Suggests new `requests` and `limits` based on historic usage.
- **Security Scanning**: Checks for privileged containers or root users.

## 3. 🧪 Manual Verification Checklist

Run these standard commands if AI agents are unavailable:

1. **Check Pods**: `kubectl get pods`
2. **Check Services**: `kubectl get svc`
3. **View Logs**: `kubectl logs -l app.kubernetes.io/name=todo-backend`
4. **Port Forward Backend**: `kubectl port-forward svc/todo-backend 8000:8000`
5. **Access Frontend**: `minikube service todo-frontend`

## 4. Spec-Driven Updates

If you need to change the infrastructure:
1. Update `speckit/phase4_spec.md`.
2. Update Helm charts in `k8s/helm/`.
3. Run `deploy_k8s.ps1` to apply changes.
4. **Do not** make ad-hoc changes with kubectl if possible. Update the Spec!
