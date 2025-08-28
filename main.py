from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from dotenv import load_dotenv
import logging

from celery_app import celery_app        
from celery_worker import analyze_document_task
from celery.result import AsyncResult
from litellm import RateLimitError

load_dotenv()
print("Loaded API Key starts with:", os.getenv("OPENAI_API_KEY")[:8])

app = FastAPI(title="Financial Document Analyzer")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_QUERY = (
    "Extract key financial metrics (revenue, profit, cash flow), "
    "identify risks, and provide concise investment recommendations. "
    "Return results in structured JSON with fields: metrics, risks, recommendations."
)

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default=DEFAULT_QUERY)
):
    """Enqueue financial document analysis via Celery"""
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    os.makedirs("data", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if not query or query.strip() == "":
        query = DEFAULT_QUERY

    try:
        # Enqueue Celery task
        task = analyze_document_task.delay(
            file_path=file_path,
            query=query.strip(),
            file_name=file.filename
        )
        return {
            "status": "queued",
            "task_id": task.id,
            "file_processed": file.filename
        }

    except RateLimitError as e:
        logger.warning(f"OpenAI API quota exceeded: {e}")
        raise HTTPException(
            status_code=429,
            detail="OpenAI API quota exceeded. Please try again later."
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error enqueueing analysis task: {str(e)}"
        )

@app.get("/result/{task_id}")
def get_result(task_id: str):
    """Check status or get result of an analysis task"""
    task_result = AsyncResult(task_id, app=celery_app)   
    if task_result.state == "PENDING":
        return {"status": "pending"}
    elif task_result.state == "SUCCESS":
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "failed", "error": str(task_result.result)}
    else:
        return {"status": task_result.state, "result": task_result.result}
