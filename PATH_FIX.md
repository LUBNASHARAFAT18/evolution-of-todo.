**Ghabrayein nahi, yeh bas "Path" ka issue hai.**

Kyunki aapne abhi Minikube install kiya hai, purane Terminal window ko pata nahi hai ki Minikube kahan hai.

**Solution 1 (Recommended):**
Apna VS Code ya PowerShell window **band karke dobara kholein** (Restart Terminal).

**Solution 2 (Quick Fix):**
Maine `deploy_k8s.ps1` script update kar di hai taaki woh khud Minikube ko dhoond le. 

Ab dobara try karein:
```powershell
.\deploy_k8s.ps1
```
