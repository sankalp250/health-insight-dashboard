# 🔧 Groq API Key Fix Guide

## Issues Fixed

1. ✅ **API Key Error Handling** - Better error messages for invalid keys
2. ✅ **Sidebar Navigation** - Now works with smooth scrolling to sections
3. ✅ **Model Name** - Using correct Groq model name
4. ✅ **Section IDs** - Added proper section IDs for navigation

## How to Fix Your Groq API Key

### Step 1: Verify Your API Key

Run this script to check your API key:

```powershell
cd D:\health-insight-dashboard\backend
.\.venv\Scripts\Activate.ps1
python check_groq_key.py
```

This will tell you if:
- ✅ Your API key is found
- ✅ Your API key is valid
- ✅ The model is available

### Step 2: Fix Common Issues

**Problem: Invalid API Key (401 Error)**

1. **Get a new API key:**
   - Go to https://console.groq.com/
   - Login to your account
   - Navigate to API Keys
   - Create a new API key
   - **Copy it immediately** (it's only shown once!)

2. **Update backend/.env:**
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
   
   **IMPORTANT:**
   - No spaces before or after the `=`
   - No quotes around the key
   - No extra characters
   - The key should start with `gsk_`

3. **Restart backend server:**
   ```powershell
   # Stop current server (Ctrl+C)
   cd D:\health-insight-dashboard\backend
   .\.venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload --port 8080
   ```

### Step 3: Test the Fix

1. **Restart frontend** (if running):
   ```powershell
   # Stop current frontend (Ctrl+C)
   cd D:\health-insight-dashboard\frontend
   npm run dev
   ```

2. **Test AI Chat:**
   - Open http://localhost:3000
   - Go to "AI Insights" section
   - Try asking: "Show me top brands in Asia"
   - Should get a proper response (not an error)

## Sidebar Navigation - Now Working!

The sidebar navigation now works properly:

- **Dashboard** - Scrolls to filters and KPIs
- **Analytics** - Scrolls to charts section
- **Trends** - Scrolls to predictions section
- **Insights** - Scrolls to AI chat section

Click any item in the sidebar and it will smoothly scroll to that section!

## Model Name

The model name `llama-3.1-70b-versatile` is correct for Groq API. If you get errors about the model, it might be:
- API key doesn't have access to this model
- Model name changed (check Groq docs)
- API key is invalid

## Still Having Issues?

1. **Check backend/.env file exists:**
   ```powershell
   Test-Path D:\health-insight-dashboard\backend\.env
   ```

2. **Check API key format:**
   ```powershell
   Get-Content D:\health-insight-dashboard\backend\.env
   ```
   Should show: `GROQ_API_KEY=gsk_...`

3. **Check backend logs:**
   - Look at the terminal running uvicorn
   - Check for error messages about API key

4. **Test API key directly:**
   ```powershell
   cd D:\health-insight-dashboard\backend
   .\.venv\Scripts\Activate.ps1
   python check_groq_key.py
   ```

## Quick Checklist

- [ ] API key is in `backend/.env` file
- [ ] API key has no spaces or quotes
- [ ] API key starts with `gsk_`
- [ ] Backend server restarted after adding key
- [ ] Frontend restarted
- [ ] Sidebar navigation works (click Analytics, Trends, Insights)
- [ ] AI chat responds without errors

If all checked ✅, everything should work!

