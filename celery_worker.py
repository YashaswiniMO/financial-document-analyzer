# celery_worker.py
import os
from celery_app import celery_app   
from database import SessionLocal, AnalysisResult
from crew_runner import run_crew     

@celery_app.task(bind=True)
def analyze_document_task(self, file_path: str, query: str, file_name: str = ""):
    """Celery task to run CrewAI analysis and save result to DB"""
    session = SessionLocal()
    record = AnalysisResult(file_name=file_name, query=query, status="processing")
    session.add(record)
    session.commit()
    try:
        result = run_crew(query=query, file_path=file_path)
        record.analysis = str(result)
        record.status = "completed"
        session.commit()
        return {"status": "success", "analysis_id": record.id, "analysis": str(result)}
    except Exception as e:
        record.status = "failed"
        session.commit()
        return {"status": "error", "error": str(e)}
    finally:
        session.close()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
