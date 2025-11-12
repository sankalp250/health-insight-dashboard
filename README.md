# Health Insight Dashboard - Vaccine Market Analytics Platform

A comprehensive full-stack web application for analyzing global vaccine market data with AI-powered insights. Built with FastAPI, React, and Groq AI (Llama 3.1).

## 🎯 Project Overview

This platform combines traditional dashboard functionality with cutting-edge AI capabilities:

- **Traditional Dashboard**: Interactive filters, KPIs, and 5+ data visualizations
- **AI Chat Interface**: Natural language queries about your data
- **Predictive Analytics**: ML-based market forecasts with confidence intervals
- **Smart Recommendations**: RAG-powered suggestions for data exploration

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- Pandas for data processing
- Groq API (Llama 3.1 70B) for AI features
- LangChain & LangGraph for AI orchestration
- CSV-based data storage (no database required)

**Frontend:**
- React 19 + TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Recharts for data visualization
- Axios for API communication

**Deployment:**
- Backend: Render
- Frontend: Vercel
- Docker support (optional)

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Groq API Key** ([Get one here](https://console.groq.com/))
- **Git** for version control

## 🚀 Quick Start Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/sankalp250/health-insight-dashboard.git
cd health-insight-dashboard
```

### Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   **Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

5. **Create `.env` file:**
   
   Create a file named `.env` in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   Replace `your_groq_api_key_here` with your actual Groq API key from https://console.groq.com/

6. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --port 8080
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8080
   INFO:     Application startup complete.
   ```

   **✅ Verify Backend:**
   - Open http://localhost:8080/docs to see API documentation
   - Test http://localhost:8080/healthz - should return `{"status": "ok"}`

### Step 3: Frontend Setup

1. **Open a NEW terminal window** (keep backend running)

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   VITE v7.x.x  ready in xxx ms
   ➜  Local:   http://localhost:3000/
   ```

5. **Open your browser:**
   - Navigate to http://localhost:3000
   - You should see the dashboard with data loaded

## 📊 Features

### Core Dashboard Features

- ✅ **Filter Panel**: Filter by Region, Brand, and Year
- ✅ **KPI Cards**: 
  - Total Market Size (USD)
  - Average Price (USD)
  - Total Doses Sold (Million)
  - CAGR (Compound Annual Growth Rate)
- ✅ **Interactive Charts**:
  - Market Size by Region (Bar Chart)
  - Market Trends Over Time (Line Chart)
  - Top Brands by Market Size (Horizontal Bar)
  - Average Growth Rate by Brand (Bar Chart)
  - Data Distribution by Region (Pie Chart)

### AI-Powered Features

- ✅ **AI Chat Interface**: Ask natural language questions like:
  - "Show me top brands in Asia"
  - "What are the market trends?"
  - "Compare Pfizer and Moderna"
- ✅ **Predictive Analytics**: 
  - Market forecasts for 1-5 years ahead
  - Confidence intervals
  - AI-generated insights
- ✅ **Smart Recommendations**: 
  - Context-aware suggestions for data exploration
  - RAG-powered recommendations based on current filters

### UI/UX Features

- ✅ Dark mode support
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Real-time data updates
- ✅ Loading states and error handling

## 🔌 API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /healthz` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### Data Endpoints

- `GET /api/vaccines` - Get vaccine market data
  - Query params: `region`, `brand`, `year`, `limit`, `offset`
- `GET /api/summary` - Get KPI summary metrics
  - Query params: `region`, `brand`, `year`

### AI Endpoints

- `POST /api/ai/chat` - Natural language query
  - Body: `{ "query": "your question", "region": "optional", "brand": "optional", "year": optional }`
- `GET /api/ai/predictions` - Get market predictions
  - Query params: `region`, `brand`, `years_ahead` (1-5)
- `GET /api/ai/recommendations` - Get AI recommendations
  - Query params: `region`, `brand`, `year`

## 🧪 Testing

### Test Backend

1. **Install test dependencies:**
   ```bash
   pip install requests
   ```

2. **Run test script:**
   ```bash
   python test_backend.py
   ```

   This will test all API endpoints and verify they're working correctly.

### Manual Testing

1. **Backend API:**
   - Visit http://localhost:8080/docs
   - Try the `/api/vaccines` endpoint with different filters
   - Test `/api/summary` endpoint

2. **Frontend:**
   - Open http://localhost:3000
   - Test filters (Region, Brand, Year)
   - Verify charts update
   - Test AI chat with questions
   - Check predictions panel

## 🐛 Troubleshooting

### Backend Issues

**Problem: Module not found errors**
```bash
# Solution: Reinstall dependencies
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
```

**Problem: Port 8080 already in use**
```bash
# Solution: Use a different port
uvicorn app.main:app --reload --port 8081
# Then update frontend/src/lib/api.ts to use port 8081
```

**Problem: GROQ_API_KEY not found**
- Ensure `.env` file exists in `backend/` directory
- Check that file contains: `GROQ_API_KEY=your_actual_key`
- Restart backend server after creating/updating `.env`

**Problem: Dataset not found**
- Verify `backend/data/vaccine_market_dataset.csv` exists
- Check file path in `backend/app/core/config.py`

### Frontend Issues

**Problem: Cannot find module**
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules  # or Remove-Item -Recurse node_modules on Windows
npm install
```

**Problem: API connection failed / No data showing**
- Verify backend is running on port 8080
- Check browser console (F12) for errors
- Verify `VITE_API_URL` in frontend (defaults to http://localhost:8080)
- Check CORS settings in backend

**Problem: AI features not working**
- Verify `GROQ_API_KEY` is set correctly in `backend/.env`
- Check backend terminal for API errors
- Test AI endpoint directly: http://localhost:8080/docs → `/api/ai/chat`

### Common Errors

**Error: "No data available for the selected filters"**
- This is normal if filters exclude all data
- Try clearing filters or selecting different values
- Check backend logs for data loading errors

**Error: "AI features are not available"**
- GROQ_API_KEY not configured or invalid
- Check `.env` file in backend directory
- Verify API key is correct at https://console.groq.com/

## 📁 Project Structure

```
health-insight-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # API endpoint definitions
│   │   │       ├── vaccines.py  # Vaccine data endpoints
│   │   │       ├── summary.py   # KPI summary endpoints
│   │   │       └── ai.py        # AI-powered endpoints
│   │   ├── core/
│   │   │   └── config.py        # Configuration management
│   │   ├── models/
│   │   │   └── vaccine.py       # Data models
│   │   ├── repositories/
│   │   │   └── vaccine_repository.py  # Data access layer
│   │   ├── services/
│   │   │   ├── vaccine_service.py     # Business logic
│   │   │   └── ai_service.py         # AI service layer
│   │   └── main.py              # FastAPI application
│   ├── data/
│   │   └── vaccine_market_dataset.csv  # Dataset
│   ├── tests/
│   │   └── test_api.py          # API tests
│   ├── .env                      # Environment variables (create this)
│   └── pyproject.toml            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   │   ├── FilterPanel.tsx   # Filter controls
│   │   │   ├── KPICard.tsx       # KPI display cards
│   │   │   ├── Charts.tsx        # Data visualizations
│   │   │   ├── AIChat.tsx        # AI chat interface
│   │   │   └── Predictions.tsx   # Predictions panel
│   │   ├── lib/
│   │   │   └── api.ts            # API client
│   │   ├── App.tsx               # Main application
│   │   └── main.tsx              # Entry point
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Vite configuration
├── README.md                     # This file
├── requirements.txt              # Python dependencies
└── test_backend.py               # Backend test script
```

## 🗄️ Data Storage

**Important:** This project uses CSV file storage, not a database. The dataset is loaded into memory at startup.

- **Dataset Location**: `backend/data/vaccine_market_dataset.csv`
- **Format**: CSV with columns: region, brand, year, market_size_usd, avg_price_usd, doses_sold_million, growth_rate_percent, insight
- **No Database Required**: All data is read from CSV and filtered in-memory

For production deployments, consider migrating to PostgreSQL or another database for better performance and scalability.

## 🚢 Deployment

### Backend Deployment (Render)

1. Connect your GitHub repository to Render
2. Create a new **Web Service**
3. Configure:
   - **Build Command**: `cd backend && pip install -r ../requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
4. Add environment variable:
   - `GROQ_API_KEY` = your Groq API key
5. Deploy!

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variable:
   - `VITE_API_URL` = your backend URL (e.g., `https://your-backend.onrender.com`)
4. Deploy!

### Docker (Optional)

Docker configuration files can be added for containerized deployment. See deployment documentation for details.

## 📝 Development

### Running in Development Mode

**Backend:**
```bash
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8080
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Building for Production

**Backend:**
- No build step required (Python runs directly)

**Frontend:**
```bash
cd frontend
npm run build
```
Output will be in `frontend/dist/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Groq for providing fast AI inference
- FastAPI for the excellent web framework
- React and Vite for the modern frontend stack
- Recharts for beautiful data visualizations

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for health data analytics**
