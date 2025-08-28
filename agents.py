## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM
# ✅ Import correct tools
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

# Load LLM
llm = LLM(model="gpt-4o-mini" , temperature=0.2)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze uploaded financial reports, extract key financial metrics, "
         "and provide evidence-based investment insights aligned with the query.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with deep experience in reading corporate "
        "earnings reports and market trends. You focus on accuracy, regulatory compliance, "
        "and actionable insights. Your role is to provide clear and structured recommendations."
    ),
    tools=[read_data_tool, analyze_investment_tool],   # ✅ Use your defined tools
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the uploaded document is a valid financial report and confirm readability.",
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in financial document verification. Your role is to ensure the document "
        "is a legitimate financial report (PDF, annual report, quarterly filing) and validate "
        "the structure before further analysis."
    ),
    tools=[read_data_tool],   # ✅ Document verifier should at least use the reader
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# Creating an investment advisor agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide tailored investment recommendations based strictly on extracted financial "
         "data and market conditions.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a licensed investment advisor with 15+ years of experience in equity research, "
        "portfolio management, and compliance. Your responsibility is to recommend structured "
        "investment strategies aligned with risk profile and financial performance."
    ),
    tools=[analyze_investment_tool],   # ✅ Give the advisor the analysis tool
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)

# Creating a risk assessor agent
risk_assessor = Agent(
    role="Risk Management Expert",
    goal="Perform balanced risk assessments of financial reports, highlighting potential threats, "
         "uncertainties, and opportunities.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management expert with extensive background in portfolio risk analysis "
        "and credit assessment. You evaluate financial documents objectively, categorizing risks "
        "into low, medium, or high, and providing mitigation strategies."
    ),
    tools=[create_risk_assessment_tool],   # ✅ Give the risk assessor the risk tool
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)
