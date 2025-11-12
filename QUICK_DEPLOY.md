# ⚡ Quick Deployment Guide

Fast deployment steps for Health Insight Dashboard.

## 🎯 Prerequisites

- GitHub repository pushed
- Render account (free tier works)
- Vercel account (free tier works)
- Groq API key

## 📦 Step 1: Deploy Backend (Render) - 5 minutes

1. **Go to Render:**
   - Visit https://dashboard.render.com
   - Sign up/Login (use GitHub for easy connection)

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub → Select `health-insight-dashboard` repository
   - Click "Connect"

3. **Configure (Auto-detected from render.yaml):**
   - **Name:** `health-insight-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt` (auto-filled)
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` (auto-filled)

4. **Add Environment Variable:**
   - Scroll to "Environment Variables"
   - Click "Add Environment Variable"
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key from https://console.groq.com/

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for first deployment
   - **Copy your service URL** (e.g., `https://health-insight-backend.onrender.com`)

6. **Verify:**
   - Visit: `https://your-backend-url.onrender.com/docs`
   - Should see API documentation
   - Test: `https://your-backend-url.onrender.com/healthz`

## 🎨 Step 2: Deploy Frontend (Vercel) - 3 minutes

1. **Go to Vercel:**
   - Visit https://vercel.com
   - Sign up/Login (use GitHub for easy connection)

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Import `health-insight-dashboard` repository
   - Click "Import"

3. **Configure (IMPORTANT - Set Root Directory):**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` ⚠️ **MUST SET THIS MANUALLY**
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   
   **Note:** Vercel may not auto-detect the root directory. You MUST manually set:
   - Click "Settings" or "Configure Project"
   - Find "Root Directory" setting
   - Set it to: `frontend`
   - Save changes

4. **Add Environment Variable:**
   - Scroll to "Environment Variables"
   - Click "Add"
   - Key: `VITE_API_URL`
   - Value: Your Render backend URL (from Step 1)
     - Example: `https://health-insight-backend.onrender.com`

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment
   - **Copy your frontend URL** (e.g., `https://health-insight-dashboard.vercel.app`)

6. **Verify:**
   - Visit your Vercel URL
   - Dashboard should load
   - Check browser console (F12) for any errors
   - Test filters and AI chat

## ✅ Post-Deployment Checklist

- [ ] Backend accessible at Render URL
- [ ] Frontend accessible at Vercel URL
- [ ] API docs working: `https://your-backend.onrender.com/docs`
- [ ] Health check working: `https://your-backend.onrender.com/healthz`
- [ ] Frontend loads dashboard
- [ ] Filters work
- [ ] Charts display
- [ ] AI chat responds (if API key is set)
- [ ] Predictions show data

## 🔧 Troubleshooting

### Backend not deploying?
- Check Render logs for errors
- Verify `requirements.txt` is in root directory
- Ensure `GROQ_API_KEY` is set (can be empty for testing)

### Frontend can't connect to backend?
- Verify `VITE_API_URL` is set correctly in Vercel
- Check CORS settings (backend allows all origins by default)
- Test backend URL directly in browser

### CORS errors?
- Backend already configured to allow all origins
- If issues persist, update `backend/app/main.py` CORS settings

## 🎉 Done!

Your application is now live:
- **Backend:** `https://your-backend.onrender.com`
- **Frontend:** `https://your-frontend.vercel.app`

Share these URLs in your assignment submission!

