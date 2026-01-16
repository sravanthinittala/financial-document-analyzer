## Importing libraries and files
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import search_tool, FinancialDocumentTool, InvestmentTool, RiskTool

load_dotenv()

# Loading LLM
llm = LLM(
    model="gpt-3.5-turbo",
    temperature=0.7,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Experienced Financial Analyst",
    goal="Provide investment advice that accurately and factually answers the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with years of experience in evaluating corporate financial reports."
        "You have a deep understanding of financial statements, ratios, and market trends."
        "Your analyses are always grounded in factual data and regulatory compliance."
        "You prioritize accuracy and clarity in your investment recommendations."
        "You avoid speculation and focus on delivering well-reasoned insights based on the financial document."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="""Determine whether the uploaded PDF is a legitimate corporate financial document.
        Verify the presence of standard financial sections and provide a structured validation result.""",
    verbose=True,
    memory=False,
    backstory=(
        "You are a financial compliance analyst responsible for validating documents before analysis. "
        "You check for standard financial reporting structures such as income statements, balance sheets, "
        "cash flow statements, and management discussion sections. "
        "You do not perform financial analysis or make assumptions beyond the document content."
    ),
    llm=llm,
    tools=[FinancialDocumentTool.read_data_tool],
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Professional Investment Advisor",
    goal="""Analyze the financial data extracted from the document.
    Provide clear and actionable investment recommendations based on the actual metrics and trends.
    Avoid speculation and focus on verified data-driven advice that aligns with the user's query: {query}
    Explain the rationale behind each recommendation using concrete financial data.""",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified investment advisor with experience and expertise in portfolio management."
        "You base your investment advice on solid financial analysis and market research."
        "Your recommendations are realistic, actionable, and tailored to the user's query."
        "You understand various investment vehicles and can tailor advice to different risk profiles."
        "You prioritize the client's financial well-being and long-term growth."
        "You explain your reasoning clearly and concisely, avoiding any invented numbers."
        "You comply with all financial regulations and ethical standards."
    ),
    llm=llm,
    tools=[InvestmentTool.analyze_investment_tool, search_tool],
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Professional Financial Risk Assessor",
    goal="""Analyze the verified financial document data and extracted metrics to identify potential financial and operational risks.
Provide a comprehensive risk assessment report highlighting key risk areas, mitigation strategies, and recommendations for risk management.
Evaluate risk exposure such as leverage ratios, liquidity risks, market volatility, and operational vulnerabilities.
Ensure all assessments are based on the actual data from the financial document and avoid speculation.""",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial risk assessor with expertise in identifying and mitigating financial risks."
        "You have a deep understanding of risk management frameworks and regulatory requirements."
        "You analyze financial documents to identify key risk indicators such as high debt, declining margins, liquidity issues, or market exposure."
        "You communicate complex risk concepts clearly and provide actionable recommendations."
        "You prioritize accuracy and compliance in all your evaluations and never invent figures."
    ),
    llm=llm,
    tools=[RiskTool.create_risk_assessment_tool],
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
