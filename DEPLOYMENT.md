# 🚀 Deployment Guide

Complete guide for deploying Health Insight Dashboard to production.

## 📋 Prerequisites

- GitHub account with repository access
- Render account (for backend)
- Vercel account (for frontend)
- Groq API key

## 🐳 Docker Deployment (Local/Server)

### Build and Run with Docker Compose

1. **Create `.env` file in project root:**
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

2. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Individual Docker Commands

**Backend:**
```bash
cd backend
docker build -t health-insight-backend .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key health-insight-backend
```

**Frontend:**
```bash
cd frontend
docker build -t health-insight-frontend .
docker run -p 3000:80 -e VITE_API_URL=http://your-backend-url health-insight-frontend
```

## ☁️ Render Deployment (Backend)

### Step 1: Prepare Repository

1. Ensure `render.yaml` is in the root directory
2. Ensure `requirements.txt` is in the root directory
3. Commit and push to GitHub

### Step 2: Deploy on Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Sign up/Login

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `health-insight-dashboard`

3. **Configure Service:**
   - **Name:** `health-insight-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** Leave empty (or set to `backend` if needed)

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add: `GROQ_API_KEY` = your Groq API key
   - Add: `PYTHON_VERSION` = `3.11.0`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the service URL (e.g., `https://health-insight-backend.onrender.com`)

### Step 3: Verify Backend

- Visit: `https://your-backend-url.onrender.com/docs`
- Test: `https://your-backend-url.onrender.com/healthz`
- Should return: `{"status": "ok"}`

## ⚡ Vercel Deployment (Frontend)

### Step 1: Prepare Repository

1. Ensure `vercel.json` is in the root directory
2. Ensure frontend code is in `frontend/` directory
3. Commit and push to GitHub

### Step 2: Deploy on Vercel

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com
   - Sign up/Login with GitHub

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Import your GitHub repository: `health-insight-dashboard`

3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

4. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = your Render backend URL
     - Example: `https://health-insight-backend.onrender.com`

5. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note the frontend URL (e.g., `https://health-insight-dashboard.vercel.app`)

### Step 3: Verify Frontend

- Visit your Vercel URL
- Check that dashboard loads
- Test API connection (should connect to Render backend)

## 🔧 Post-Deployment Configuration

### Update CORS (if needed)

If frontend can't connect to backend, update `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:3000",  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update Frontend API URL

If you need to change the backend URL after deployment:

1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Update `VITE_API_URL`
5. Redeploy

## 📝 Deployment Checklist

### Backend (Render)
- [ ] Repository pushed to GitHub
- [ ] `render.yaml` in root directory
- [ ] `requirements.txt` in root directory
- [ ] Render service created
- [ ] `GROQ_API_KEY` environment variable set
- [ ] Service deployed and running
- [ ] Health check passing: `/healthz`
- [ ] API docs accessible: `/docs`

### Frontend (Vercel)
- [ ] Repository pushed to GitHub
- [ ] `vercel.json` in root directory
- [ ] Vercel project created
- [ ] `VITE_API_URL` environment variable set to Render backend URL
- [ ] Project deployed
- [ ] Frontend loads correctly
- [ ] API calls work (check browser console)

## 🐛 Troubleshooting

### Backend Issues

**Problem: Build fails on Render**
- Check `requirements.txt` is in root directory
- Verify Python version (3.11+)
- Check build logs in Render dashboard

**Problem: Service crashes**
- Check environment variables are set
- Review logs in Render dashboard
- Verify `GROQ_API_KEY` is correct

**Problem: CORS errors**
- Update `allow_origins` in `backend/app/main.py`
- Add your Vercel frontend URL

### Frontend Issues

**Problem: Build fails on Vercel**
- Check `vercel.json` configuration
- Verify `package.json` exists in `frontend/`
- Check build logs in Vercel dashboard

**Problem: API connection fails**
- Verify `VITE_API_URL` is set correctly
- Check backend is running on Render
- Verify CORS settings in backend

**Problem: 404 errors on routes**
- Ensure `vercel.json` has rewrite rules
- Check `nginx.conf` if using Docker

## 🔐 Security Notes

1. **Never commit API keys:**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Production CORS:**
   - Restrict `allow_origins` to your frontend URL only
   - Don't use `["*"]` in production

3. **Environment Variables:**
   - Keep secrets in deployment platform (Render/Vercel)
   - Never expose in client-side code

## 📊 Monitoring

### Render Monitoring
- View logs: Render Dashboard → Your Service → Logs
- Monitor uptime: Render Dashboard → Your Service → Metrics

### Vercel Monitoring
- View logs: Vercel Dashboard → Your Project → Deployments → View Function Logs
- Monitor analytics: Vercel Dashboard → Analytics

## 🎉 Success!

Once deployed:
- ✅ Backend running on Render
- ✅ Frontend running on Vercel
- ✅ API calls working
- ✅ All features functional

Share your deployed URLs:
- Backend: `https://your-backend.onrender.com`
- Frontend: `https://your-frontend.vercel.app`

