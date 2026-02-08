**Check karne ke liye maine ek simple script banayi hai.**

Bas is command ko run karein:

```powershell
.\verify_k8s.ps1
```

**Output mein yeh dekhein:**
1.  **Pods Status**:
    Likha hona chahiye: `STATUS: Running` aur `READY: 1/1`
    *(Iska matlab app sahi chal raha hai)*

2.  **Services**:
    Aapko `http://` wale URLs dikhenge jahan aap click karke app khol sakte hain.

**Alternatively (Manual Commands):**
Agar script na chale, to yeh type karein:
- `minikube kubectl -- get pods`
- `minikube service list`
