# 🚀 Quick Start Guide - Run the Project

Follow these steps to run the Health Insight Dashboard locally.

## Step 1: Setup Backend

### 1.1 Create Environment File

Create a file named `.env` in the `backend/` directory with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Where to get Groq API Key:**
1. Go to https://console.groq.com/
2. Sign up/Login
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it in the `.env` file

### 1.2 Activate Virtual Environment

Open PowerShell/Terminal in the project root and run:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.3 Install Dependencies (if not already done)

```powershell
pip install fastapi uvicorn pandas pydantic pydantic-settings python-multipart groq langchain langchain-groq langgraph scikit-learn numpy
```

### 1.4 Start Backend Server

```powershell
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**✅ Test Backend:**
- Open browser: http://localhost:8000/docs
- You should see the FastAPI documentation
- Try the `/healthz` endpoint to verify it's working

---

## Step 2: Setup Frontend

### 2.1 Open New Terminal Window

Keep the backend running, open a **NEW** terminal window.

### 2.2 Navigate to Frontend

```powershell
cd D:\health-insight-dashboard\frontend
```

### 2.3 Install Dependencies (if not already done)

```powershell
npm install
```

### 2.4 Start Frontend Server

```powershell
npm run dev
```

You should see:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

---

## Step 3: Test the Application

1. **Open Browser:** http://localhost:3000

2. **What You Should See:**
   - ✅ Dashboard with filters (Region, Brand, Year)
   - ✅ 4 KPI cards showing metrics
   - ✅ 5+ interactive charts
   - ✅ AI Chat interface (bottom left)
   - ✅ Predictions panel (bottom right)

3. **Test Filters:**
   - Select a region (e.g., "Asia")
   - Select a brand (e.g., "Pfizer")
   - Charts and KPIs should update automatically

4. **Test AI Chat:**
   - Type: "Show me top brands in Asia"
   - You should get an AI response with visualization suggestions

5. **Test Predictions:**
   - The predictions panel should show forecast charts
   - Try changing the "years ahead" dropdown

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error: Module not found**
```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate.ps1
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: Port 8000 already in use**
```powershell
# Use a different port
uvicorn app.main:app --reload --port 8001
# Then update frontend/.env to use port 8001
```

**Error: GROQ_API_KEY not found**
- Make sure `.env` file exists in `backend/` directory
- Check that the file contains: `GROQ_API_KEY=your_actual_key`
- Restart the backend server after creating/updating `.env`

### Frontend Won't Start

**Error: Cannot find module**
```powershell
# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install
```

**Error: API connection failed**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify `VITE_API_URL` in frontend (defaults to http://localhost:8000)

### AI Features Not Working

- Verify GROQ_API_KEY is set correctly in `backend/.env`
- Check backend logs for API errors
- Test the endpoint directly: http://localhost:8000/docs → `/api/ai/chat`

---

## 📝 Quick Commands Reference

**Backend:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

**Stop Servers:**
- Press `Ctrl+C` in each terminal window

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can see dashboard with charts
- [ ] Filters work and update data
- [ ] AI Chat responds to queries
- [ ] Predictions panel shows forecasts

If all checkboxes are ✅, you're good to go! 🎉

