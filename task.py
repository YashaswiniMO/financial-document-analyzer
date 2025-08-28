## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

## Task: Analyze financial document
analyze_financial_document = Task(
    description=(
        "Carefully review the uploaded financial document and analyze it based on the user's query: {query}. "
        "Extract key metrics such as revenue, profit, EPS, liabilities, and cash flow. "
        "Summarize findings in a structured and clear format."
    ),
    expected_output=(
        "A structured financial analysis including:\n"
        "- Key highlights (revenues, profits, expenses, EPS, etc.)\n"
        "- Trends or anomalies\n"
        "- Possible red flags\n"
        "- Summary insights relevant to the query"
    ),
    agent=financial_analyst,
    tools=[read_data_tool],
    async_execution=False,
)

## Task: Investment analysis
investment_analysis = Task(
    description=(
        "Using insights extracted from the financial document, evaluate the company’s "
        "investment potential. Align the recommendations with the user's query: {query}. "
        "Provide risk-adjusted buy/hold/sell advice and possible growth opportunities."
    ),
    expected_output=(
        "An investment strategy report including:\n"
        "- Company strengths and weaknesses\n"
        "- Market outlook\n"
        "- Buy/Hold/Sell recommendation\n"
        "- Potential opportunities (e.g., sectors, products)\n"
        "- Risks investors should be aware of"
    ),
    agent=investment_advisor,
    tools=[read_data_tool, search_tool, analyze_investment_tool],
    async_execution=False,
)

## Task: Risk assessment
risk_assessment = Task(
    description=(
        "Evaluate the risk profile of the company based on financial document findings. "
        "Highlight operational, financial, and market risks. "
        "Categorize risks into Low, Medium, or High, and provide recommendations for mitigation."
    ),
    expected_output=(
        "A structured risk assessment report including:\n"
        "- Identified risks (financial, operational, market)\n"
        "- Risk level (Low/Medium/High)\n"
        "- Mitigation strategies\n"
        "- Overall company risk profile"
    ),
    agent=risk_assessor,
    tools=[read_data_tool, create_risk_assessment_tool],
    async_execution=False,
)

## Task: Document verification
verification = Task(
    description=(
        "Check the uploaded document to confirm if it is a financial report. "
        "Validate that it contains financial terms, tables, or corporate metrics. "
        "If invalid, flag the document and provide reasoning."
    ),
    expected_output=(
        "A verification summary including:\n"
        "- Whether the document is a valid financial report (Yes/No)\n"
        "- Key checks performed (e.g., presence of balance sheet, P&L)\n"
        "- Any issues or warnings"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)
