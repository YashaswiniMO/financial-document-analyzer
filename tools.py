import os
from dotenv import load_dotenv
from crewai.tools import tool           
from crewai_tools import SerperDevTool  
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()


search_tool = SerperDevTool()

# ---- PDF Reader Tool ----
@tool("Read Financial Document")
def read_data_tool(path: str = "data/sample.pdf") -> str:
    """
    Reads and extracts text from a PDF file.
    """
    if not os.path.exists(path):
        return f"Error: File not found at {path}"

    try:
        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            content = data.page_content.strip()
            content = " ".join(content.split())  # clean whitespace
            full_report += content + "\n"

        return full_report.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# ---- Investment Analysis Tool ----
@tool("Investment Analysis")
def analyze_investment_tool(financial_document_data: str) -> str:
    """
    Performs a placeholder investment analysis on document data.
    """
    if not financial_document_data:
        return "No financial data provided."

    return (
        "Investment Analysis Report:\n"
        "- Company financials reviewed.\n"
        "- Revenue, profits, and liabilities extracted.\n"
        "- Buy/Hold/Sell recommendation pending detailed model integration."
    )


# ---- Risk Assessment Tool ----
@tool("Risk Assessment")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """
    Performs a placeholder risk assessment.
    """
    if not financial_document_data:
        return "No financial data provided."

    return (
        "Risk Assessment Report:\n"
        "- Identified potential operational and market risks.\n"
        "- Risk profile categorized as Medium.\n"
        "- Mitigation strategies: Diversification, liquidity management."
    )
