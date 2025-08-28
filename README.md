# Financial Document Analyzer (CrewAI-based)

A robust system to analyze financial documents, extract key metrics, provide investment insights, and perform risk assessment using CrewAI agents.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Bugs Found & Fixes](#bugs-found--fixes)  
3. [Setup & Installation](#setup--installation)  
4. [Usage Instructions](#usage-instructions)  
5. [API Documentation](#api-documentation)  
6. [Bonus Features](#bonus-features)  
7. [Running Bonus Features](#running-bonus-features)  

---

## 🚀 Project Overview

This project performs:

- 📑 **Document parsing** – Reads PDF financial reports.  
- 📈 **Financial analysis** – Extracts revenue, profit, cash flow, and other key metrics.  
- 💡 **Investment advice** – Generates structured, evidence-based recommendations.  
- ⚠️ **Risk assessment** – Evaluates potential financial risks with mitigation strategies.  
- ✅ **Validation** – Ensures uploaded documents are legitimate financial reports.  

---

## 🛠 Tech Stack

- **Backend:** Python, FastAPI  
- **Agents & AI:** CrewAI (LLM agents)  
- **Tools:** PDFReader, custom Financial/Investment/Risk Tools  
- **Database:** PostgreSQL/MySQL via SQLAlchemy  
- **Concurrency:** Celery + Redis for async task handling  

---

## 🐞 Bugs Found & Fixes

### main.py
| Bug | Explanation | Fix |
|-----|-------------|-----|
| Function name conflict | Imported `analyze_financial_document` and redefined it as FastAPI route | Renamed endpoint to `analyze_document` |
| Crew kickoff misuse | `financial_crew.kickoff({'query': query})` throws error | Use `inputs={"query": query, "file_path": file_path}` |
| File path not passed | Task did not receive file path | Forwarded `file_path` to Crew input |
| Async vs Sync | `run_crew()` is sync but called from async route | Used `loop.run_in_executor` |
| Cleanup timing | File deleted before task completion | Delete file in background after processing |
| Generic default query | Vague prompt wastes tokens | Replaced with structured, scoped default query |

### agents.py
- **Fixed LLM initialization** (`LLM(model="gpt-4", temperature=0.2)`)  
- **Corrected tool argument** (`tools=[...]`)  
- **Rewrote prompts** (evidence-based, compliance-friendly)  
- **Added memory** (`memory=True`)  

### task.py
- Assigned **correct agents** per task (verifier, investment_advisor, risk_assessor)  
- Matched tools selectively (not all tasks use `read_data_tool`)  
- Rewrote structured, realistic prompts  

### tools.py
- Fixed **PDF import** (`from crewai_tools import PDFReaderTool`)  
- Fixed async mismatches  
- Optimized whitespace cleanup (`" ".join(processed_data.split())`)  
- Added structured **investment/risk placeholder tools**  
- Standardized naming conventions  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone repository
```bash
git clone https://github.com/your-username/financial-document-analyzer.git
cd financial-document-analyzer
```

### 2️⃣ Create Python environment
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API keys
Create a `.env` file in the project root and set your API key:
```env
CREWAI_API_KEY=your_api_key_here
```

### 5️⃣ Run FastAPI server
```bash
uvicorn main:app --reload
```

Server will start at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📌 Usage Instructions

### 🔹 1. Synchronous Analysis (`/analyze`)
Upload a PDF via `POST /analyze` (with optional query).  

**Example cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
-F "file=@TSLA-Q2-2025-Update.pdf" \
-F "query=Extract metrics, risks, recommendations, and market insights"
```

**Response:**
```json
{
  "metrics": {...},
  "risks": [...],
  "recommendations": [...],
  "market_insights": [...]
}
```

---

### 🔹 2. Asynchronous Analysis (`/analyze_async`)
Handles **concurrent requests** via Celery + Redis.  

**Response (immediate):**
```json
{
  "task_id": "a1b2c3d4e5",
  "status": "Processing"
}
```

Check status:  
```bash
GET /task_status/a1b2c3d4e5
```

**Completed Response:**
```json
{
  "task_id": "a1b2c3d4e5",
  "status": "SUCCESS",
  "result": {
    "metrics": {...},
    "risks": [...],
    "recommendations": [...],
    "market_insights": [...]
  }
}
```

---

## 📖 API Documentation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Upload PDF and get immediate analysis |
| `/analyze_async` | POST | Upload PDF, process asynchronously, return task ID |
| `/task_status/{task_id}` | GET | Check status and retrieve async results |

---

##  Bonus Features

### 1️⃣ Queue Worker Model
- Celery + Redis handles **concurrent requests**  
- FastAPI pushes tasks → Celery workers execute CrewAI agents  

### 2️⃣ Database Integration
- Stores analysis results, user data, and file metadata  
- Recommended: **SQLite via SQLAlchemy**  

---

## ▶️ Running Bonus Features

### Start Redis server
```bash
redis-server
```

### Start Celery worker
```bash
celery -A celery_worker worker --loglevel=info
```

### Start FastAPI server
```bash
uvicorn main:app --reload
```

- Use `/analyze_async` endpoint  
- Results stored in DB, retrievable via **task ID** or DB query  

---


Market insights
