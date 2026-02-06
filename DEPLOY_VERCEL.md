# Deploying to Vercel

Since I cannot create an account for you due to security restrictions, please follow these steps to deploy your application.

## Step 1: Create Vercel Account
1. Go to [https://vercel.com/signup](https://vercel.com/signup).
2. Click **"Continue with GitHub"**.
3. Authorize Vercel to access your GitHub account.

## Step 2: Deploy Frontend (Next.js)
1. In your Vercel Dashboard, click **"Add New..."** -> **"Project"**.
2. Find the repository `LUBNASHARAFAT18/evolution-of-todo` and click **"Import"**.
3. **Configure Project**:
   - **Framework Preset**: Next.js
   - **Root Directory**: Click "Edit" and select `frontend`.
   - **Environment Variables**:
     - Key: `NEXT_PUBLIC_API_URL`
     - Value: `https://your-backend-project.vercel.app` (You will update this after deploying Backend, for now use generic placeholder or skip).
4. Click **Deploy**.

## Step 3: Deploy Backend (FastAPI)
1. Go back to Dashboard, click **"Add New..."** -> **"Project"**.
2. **Import the SAME repository** `LUBNASHARAFAT18/evolution-of-todo` again.
3. **Configure Project**:
   - **Project Name**: `evolution-of-todo-backend` (or similar)
   - **Root Directory**: Leave as `root` ( `.`).
   - **Build Command**: Leave default (Vercel detects Python).
   - **Environment Variables**:
     - Key: `GEMINI_API_KEY`
     - Value: (Paste your actual Gemini API Key here)
     - Key: `PYTHON_VERSION` (Optional, defaults to 3.9)
4. Click **Deploy**.

## Step 4: Connect Them
1. Once Backend is deployed, copy its URL (e.g., `https://evolution-of-todo-backend.vercel.app`).
2. Go to your **Frontend** project settings in Vercel.
3. Go to **Environment Variables**.
4. Add/Update `NEXT_PUBLIC_API_URL` with the Backend URL.
5. Go to **Deployments** tab and **Redeploy** the latest commit for changes to take effect.

## Project Configuration Updates
I have automatically prepared your project for this deployment:
- ✅ Created `api/index.py` entry point for Vercel.
- ✅ Added `requirements.txt` to root for Python dependencies.
- ✅ Configured `vercel.json` for API rewrites.

You are ready to go!
