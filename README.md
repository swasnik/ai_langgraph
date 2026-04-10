# Financial Analysis Agent

## Overview
This project implements a financial analysis agent using a Directed Acyclic Graph (DAG) workflow.
The agent performs tasks such as data gathering, document parsing and report generation. 
It leverages tools like OpenAI's GPT models, Tavily search results.

## Features
- **Research Node**: Gathers data from web searches and PDFs.
- **Review Node**: Evaluates data sufficiency and checks for hallucinations.
- **Report Node**: Generates structured financial reports.

## Requirements
- Python 3.8+
- Install dependencies using the `requirements.txt` file:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
1. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
2. Run the `fin.py` script to invoke the workflow:
   ```bash
   python fin.py
   ```
3. The agent will process the query and generate a financial report.

## LangSmith trace
<img width="1351" height="843" alt="langsmith_trace" src="https://github.com/user-attachments/assets/af5885ad-8ebd-4e8c-9771-226a63bab842" />


## File Structure
- **fin.py**: Main script containing the DAG workflow and agent logic.
- **requirements.txt**: Lists all Python dependencies.

## Example Query
The agent can handle queries like:
```
Compare Q1 2026 Tesla vs BYD financials and supply chain risks.
```

## Notes
- Ensure that the required API keys are valid and have sufficient quota.
- The agent uses OpenAI's GPT-4 model for language processing.

## License
This project is licensed under the MIT License.
