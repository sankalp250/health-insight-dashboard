# 🚀 How to Run the Project

## Quick Steps

### 1️⃣ Edit Backend Environment File

Open `backend/.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

**Get your API key:** https://console.groq.com/

---

### 2️⃣ Start Backend (Terminal 1)

```powershell
# Navigate to backend
cd D:\health-insight-dashboard\backend

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start server
uvicorn app.main:app --reload --port 8000
```

**✅ Success indicators:**
- You see: `INFO: Uvicorn running on http://127.0.0.1:8000`
- Open http://localhost:8000/docs to see API documentation

---

### 3️⃣ Start Frontend (Terminal 2 - NEW WINDOW)

```powershell
# Navigate to frontend
cd D:\health-insight-dashboard\frontend

# Start dev server
npm run dev
```

**✅ Success indicators:**
- You see: `Local: http://localhost:3000/`
- Open http://localhost:3000 in your browser

---

### 4️⃣ Test Everything

1. **Backend Test:**
   ```powershell
   # In a new terminal
   python test_backend.py
   ```

2. **Frontend Test:**
   - Open http://localhost:3000
   - You should see:
     - ✅ Dashboard with filters
     - ✅ 4 KPI cards
     - ✅ 5+ charts
     - ✅ AI Chat (bottom left)
     - ✅ Predictions (bottom right)

3. **Try These:**
   - Filter by region: Select "Asia"
   - Filter by brand: Select "Pfizer"
   - Ask AI: "Show me top brands in Asia"
   - Check predictions panel

---

## 🐛 Common Issues

### Backend won't start

**Error: Module not found**
```powershell
# Reinstall dependencies
cd backend
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pandas pydantic pydantic-settings python-multipart groq langchain langchain-groq langgraph scikit-learn numpy
```

**Error: Port 8000 in use**
```powershell
# Use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start

**Error: Cannot find module**
```powershell
cd frontend
npm install
```

**Error: API connection failed**
- Make sure backend is running on port 8000
- Check browser console (F12) for errors

### AI features not working

- Make sure `GROQ_API_KEY` is set in `backend/.env`
- Restart backend after adding API key
- Check backend terminal for error messages

---

## 📊 What Should Work

✅ **Backend Endpoints:**
- http://localhost:8000/healthz → `{"status": "ok"}`
- http://localhost:8000/api/vaccines → Vaccine data
- http://localhost:8000/api/summary → KPI metrics
- http://localhost:8000/api/ai/chat → AI queries

✅ **Frontend Features:**
- Filters update charts and KPIs
- AI Chat responds to questions
- Predictions show forecast charts
- Dark mode toggle works

---

## 🎯 Next Steps After Testing

Once everything works:
1. ✅ Test all filters
2. ✅ Try AI chat with different questions
3. ✅ Check predictions accuracy
4. ✅ Test dark mode
5. ✅ Verify responsive design (resize browser)

If all works, you're ready for deployment! 🚀

