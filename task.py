## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool, InvestmentTool, RiskTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="""
Analyze the verified financial document and extract meaningful financial insights that directly address the user's query: {query}. 
Focus on factual analysis of financial statements, including revenue, profitability, cash flow, balance sheet strength, and notable trends over time. 
Use external market data or context only when necessary and cite sources when used. 
Do not provide investment recommendations or risk assessments.""",
    expected_output="""
Produce a structured financial analysis that includes:
- Key financial metrics and figures referenced directly from the document
- Notable trends and period-over-period changes
- Strengths and weaknesses observed in the financial performance
- A clear, factual response to the user's query based solely on the document data
- Sources for any external market context used (if applicable)
Ensure all statements are grounded in the document data. Avoid speculation.""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""
Using the verified and analyzed financial data from the document, provide professional investment advice.
Your analysis should:
- Assess the company's financial health and growth prospects
- Use market research and external sources (via search_tool) to contextualize performance
- Provide clear, actionable investment recommendations aligned with the user's query: {query}
- Suggest suitable investment products based on the financial data
- Clearly explain the rationale behind each recommendation
- Ensure all advice is grounded in factual data from the document and reputable sources
- Avoid speculation and do not invent any financial data
If insufficient data exists to make a recommendation, state that explicitly.
""",
    expected_output="""
- Clear Investment Recommendations: <List of recommended investment products or strategies>
- Rationale: Explanation for each recommendation based on financial data and market research
- Supporting Data: Key data points from the financial document that support the recommendations
- Market Context: Relevant market conditions influencing the recommendations
- Explicit limitations or uncertainties in the analysis
- Alignment with User Query: How the recommendations address the user's specific query
- """,
    agent=investment_advisor,
    tools=[InvestmentTool.analyze_investment_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""
Using the verified financial data from the document and extracted metrics, perform a comprehensive risk assessment.

Your responsibilities:
- Identify financial, operational, and market risks based on actual data from the document
- Evaluate risk exposure related to liquidity, leverage, profitability trends, and market conditions
- Assess how these risks may impact investors relative to the user's query: {query}
- Propose realistic and compliant risk mitigation strategies
- Avoid speculation, invented metrics, or unsupported claims

If the document lacks sufficient data to assess a specific risk category, explicitly state the limitation.
""",
    expected_output="""
- Overview of the company’s overall risk profile
- Key financial risks (e.g., liquidity risk, leverage, margin pressure)
- Operational and market risks supported by document evidence
- Risk severity assessment (low / moderate / high) with justification
- Practical mitigation strategies grounded in standard risk management practices
- Explicit assumptions and data limitations
""",
    agent=risk_assessor,
    tools=[RiskTool.create_risk_assessment_tool, search_tool],
    async_execution=False,
)

# Creating a document verification task    
verification = Task(
    description=("Read the uploaded PDF and verify whether it is a legitimate corporate financial document. "
        "Check for the presence of standard financial reporting sections such as Income Statement, "
        "Balance Sheet, Cash Flow Statement, and Management Discussion. "
        "If the document does not appear to be financial in nature, mark it as invalid."),
    expected_output="""
Return a structured validation result in JSON format with the following keys:\n
- is_valid_financial_document (boolean)\n
- document_type (string, e.g., 'Quarterly Earnings Report', 'Annual Report', or 'Unknown')\n
- detected_sections (list of strings)\n
- summary (short factual summary of the document content)\n
\nDo not perform investment analysis or risk assessment.""",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=True
)