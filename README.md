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

## Project Overview

This project is a CrewAI-powered financial document analyzer that performs:

- **Document parsing** – Reads PDF financial reports.  
- **Financial analysis** – Extracts revenue, profit, cash flow, and other key metrics.  
- **Investment advice** – Generates structured, evidence-based recommendations.  
- **Risk assessment** – Evaluates potential financial risks with mitigation strategies.  
- **Validation** – Ensures uploaded documents are legitimate financial reports.  

**Tech Stack:**

- Backend: Python, FastAPI  
- Agents & AI: CrewAI (LLM agents)  
- Tools: PDFReader, custom Financial/Investment/Risk Tools  
- Database: PostgreSQL/MySQL via SQLAlchemy  
- Concurrency: Celery + Redis for async task handling  

---

## Bugs Found & Fixes

### main.py

| Bug | Explanation | Fix |
|-----|-------------|-----|
| Function name conflict | Imported `analyze_financial_document` from task.py and redefined it as FastAPI route | Renamed endpoint to `analyze_document` |
| Crew kickoff misuse | `financial_crew.kickoff({'query': query})` throws error | Use `inputs={"query": query, "file_path": file_path}` |
| File path not passed | Task did not receive file path | Forwarded `file_path` to Crew input |
| Async vs Sync | run_crew() is sync but called from async route | Used `loop.run_in_executor` to avoid blocking |
| Cleanup timing | File deleted before task completion | Delete file in background after processing |
| Generic default query | Vague prompt wastes tokens | Replaced with scoped, structured default query |

### agents.py

| Bug | Explanation | Fix |
|-----|-------------|-----|
| LLM undefined | `llm = llm` causes NameError | Properly load LLM: `LLM(model="gpt-4", temperature=0.2)` |
| Wrong argument tool | Should be `tools=[...]` | Fixed argument name |
| Unrealistic prompts | Encourages hallucinations | Rewrote prompts: focused, evidence-based, compliance-friendly |
| Missing memory | Multi-turn tasks inconsistent | Added `memory=True` to all agents |

### task.py

| Bug | Explanation | Fix |
|-----|-------------|-----|
| Wrong agent usage | All tasks tied to financial_analyst | Assigned each task to the correct agent (`verifier`, `investment_advisor`, `risk_assessor`) |
| Tools mismatch | Every task used `read_data_tool` | Assigned tools selectively based on task needs |
| Bad prompt instructions | Encouraged hallucination | Rewritten structured, realistic instructions with expected output |

### tools.py

| Bug | Explanation | Fix |
|-----|-------------|-----|
| PDF not imported | `Pdf(file_path=path).load()` fails | Imported correct PDF reader (`from crewai_tools import PDFReaderTool`) |
| Async mismatch | Async tool not awaited | Converted to sync methods or properly awaited |
| Inefficient whitespace cleanup | O(n²) loop | Replaced with `" ".join(processed_data.split())` |
| Placeholder tools | Unimplemented investment/risk tools | Added structured placeholder outputs |
| Naming conventions | Inconsistent | Updated to match CrewAI callable tool conventions |

---

## Setup & Installation

1. **Clone repository**

```bash
git clone https://github.com/your-username/financial-document-analyzer.git
cd financial-document-analyzer

### 1. Clone Repository
```bash
git clone https://github.com/your-username/financial-document-analyzer.git
cd financial-document-analyzer
2. Create Python Environment
bash
Copy code
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure API Keys
Create a .env file in the root directory:

ini
Copy code
CREWAI_API_KEY=your_api_key_here
5. Run FastAPI Server
bash
Copy code
uvicorn main:app --reload
The server will start at:
👉 http://127.0.0.1:8000

📌 Usage Instructions
1. Synchronous Analysis (/analyze)
Upload PDF via POST /analyze

Optional query parameter

Returns structured JSON

Example Response:

json
Copy code
{
  "metrics": {...},
  "risks": [...],
  "recommendations": [...],
  "market_insights": [...]
}
Example cURL:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/analyze" \
-F "file=@TSLA-Q2-2025-Update.pdf" \
-F "query=Extract metrics, risks, recommendations, and market insights"
2. Asynchronous Analysis (/analyze_async)
Handles concurrent requests via Celery + Redis

Returns a task ID immediately

Example Response:

json
Copy code
{
  "task_id": "a1b2c3d4e5",
  "status": "Processing"
}
Check status:

json
Copy code
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
📖 API Documentation
Endpoint	Method	Description
/analyze	POST	Upload PDF and get immediate analysis
/analyze_async	POST	Upload PDF, process asynchronously
/task_status/{task_id}	GET	Check status & retrieve async results

🎯 Bonus Features
1. Queue Worker Model
Celery + Redis for concurrent request handling

FastAPI pushes tasks → Celery workers execute CrewAI agents

2. Database Integration
Stores analysis results, user data, file metadata

Recommended: PostgreSQL/MySQL via SQLAlchemy

▶️ Running Bonus Features
Start Redis
bash
Copy code
redis-server
Start Celery Worker
bash
Copy code
celery -A celery_worker worker --loglevel=info
Start FastAPI Server
bash
Copy code
uvicorn main:app --reload
Now you can:

Use /analyze_async for large-scale processing

Results will be stored in the database and retrievable via task ID

✅ Expected Features
Upload financial documents (PDF format)

AI-powered financial analysis

Investment recommendations

Risk assessment

Market insights
