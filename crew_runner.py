# crew_runner.py
from agents import financial_analyst
from task import analyze_financial_document as analyze_task
from crewai import Crew, Process

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the Crew with analyst agent and task"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_task],
        process=Process.sequential,
    )
    result = financial_crew.kickoff(inputs={"query": query, "file_path": file_path})
    return result
