# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirements.txt
```

## Changes Made

1. Fixed versions in `requirements.txt` keeping versions of crewai, crewai_tools and fastapi unchanges
2. Fixed role, goals, and backstory for the four agents
3. Fixed description and expected output for Tasks
4. Implemented simple logic for InvestmentAnalysisTool and RiskAssesmentTool
5. In the `agents.py` the llm was not defined. Defined an OpenAI model.
6. Corrected import errors in all files. 
7. Used `from langchain_community.document_loaders import PyPDFLoader as Pdf` to read PDFs in `read_data_tool`
8. Used decorator `@tool` for functions being used as tools.
9. Corrected the agents, tools and value of `async_execution` for all Tasks in tasks.py.
10. Updated README.md
11. Added `.env_template`

## Setup and Run

To setup the project run the following to install all dependencies:

```
pip install -r requirements.txt
```
Include the required API keys in a `.env` file in the root directory (ref: `.env_template`)
Then run using the following command:

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application is launched at [http://localhost:8000](http://localhost:8000)

## API Endpoints

The following API Endpoints are exposed:
1. Healthcheck (GET `/`): Displays a message if application is running
2. Document Analze (POST `/analyze`): A financial document is uploaded on which analysis is carried out.

## Assesment Instructions
### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

**Note:** Current `data/sample.pdf` is a placeholder - replace with actual Tesla financial document for proper testing.

# You're All Not Set!
🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code in each file and understand the expected behavior. There is a bug in each line of code. So be careful.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights