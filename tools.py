## Importing libraries and files
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader as Pdf
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @tool("read_data_tool")
    async def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file
        """
        
        loader = Pdf(path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            # Clean and format the financial document data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("analyze_investment_tool")
    async def analyze_investment_tool(financial_document_data):
        """
        Docstring for analyze_investment_tool
        
        :param financial_document_data: The financial document data as a string.
        :return: A dictionary containing investment insights.
        """
        # Process and analyze the financial document data
        if not financial_document_data or financial_document_data.strip() == "":
            return {"error": "No financial document data provided."}
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        
        text = processed_data.lower()

        insights = {
            "revenue_trend": "unknown",
            "profitability": "unknown",
            "cash_flow": "unknown",
            "debt_level": "unknown",
            "investment_signals": []
        }

        # --- Revenue trend ---
        if "revenue increased" in text or "revenue growth" in text:
            insights["revenue_trend"] = "growing"
            insights["investment_signals"].append("Positive revenue growth detected")
        elif "revenue declined" in text or "revenue decrease" in text:
            insights["revenue_trend"] = "declining"
            insights["investment_signals"].append("Revenue decline detected")

        # --- Profitability ---
        if "operating margin" in text or "net income" in text:
            insights["profitability"] = "profitable"
            insights["investment_signals"].append("Company reports profitability metrics")
        elif "net loss" in text:
            insights["profitability"] = "loss-making"
            insights["investment_signals"].append("Company reports net losses")

        # --- Cash flow ---
        if "positive cash flow" in text or "operating cash flow" in text:
            insights["cash_flow"] = "positive"
            insights["investment_signals"].append("Positive operating cash flow")
        elif "negative cash flow" in text:
            insights["cash_flow"] = "negative"
            insights["investment_signals"].append("Negative cash flow")

        # --- Debt ---
        if "long-term debt" in text or "total debt" in text:
            insights["debt_level"] = "present"
            insights["investment_signals"].append("Debt obligations identified")

        # --- Overall signal ---
        if insights["revenue_trend"] == "growing" and insights["profitability"] == "profitable":
            insights["overall_outlook"] = "fundamentally strong"
        elif insights["profitability"] == "loss-making":
            insights["overall_outlook"] = "high risk"
        else:
            insights["overall_outlook"] = "mixed"

        return insights

    

## Creating Risk Assessment Tool
class RiskTool:
    @tool("create_risk_assessment_tool")
    async def create_risk_assessment_tool(financial_document_data):
        """
        Docstring for create_risk_assessment_tool
        
        :param financial_document_data: Document data as a string.
        :return: A dictionary containing risk assessment.
        """
        # Process and analyze the financial document data for risks
        if not financial_document_data or financial_document_data.strip() == "":
            return {"error": "No financial document data provided."}   
        text = " ".join(financial_document_data.split()).lower()

        risks = {
            "liquidity_risk": "unknown",
            "leverage_risk": "unknown",
            "profitability_risk": "unknown",
            "market_risk": "unknown",
            "overall_risk": "unknown"
        }

        # Minimal keyword-based checks
        if "cash flow" in text and "negative" in text:
            risks["liquidity_risk"] = "high"
        if "debt" in text:
            risks["leverage_risk"] = "present"
        if "profit" in text or "loss" in text:
            risks["profitability_risk"] = "evaluated"
        if "market" in text:
            risks["market_risk"] = "considered"

        # Simple overall risk
        if risks["liquidity_risk"] == "high" or risks["leverage_risk"] == "present":
            risks["overall_risk"] = "moderate to high"
        else:
            risks["overall_risk"] = "low to moderate"

        return risks