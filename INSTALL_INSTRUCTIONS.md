**Phase 4 run karne ke liye kuch tools missing hain** (`minikube`, `helm`, `kubectl`).

Maine ek script banayi hai jo inhein install kar degi.

**Please run this command in your PowerShell (Admin recommended):**

```powershell
.\install_k8s_tools.ps1
```

**Installation ke baad:**
1.  Apna terminal/PowerShell **restart** karein (taki naye tools load ho sakein).
2.  Phir Phase 4 run karein:
    ```powershell
    .\deploy_k8s.ps1
    ```

Yeh script automatic `minikube`, `helm` aur `kubectl` download aur install kar legi.
