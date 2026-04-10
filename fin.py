import operator
from typing import Annotated, Sequence, TypedDict
from langgraph.graph import END, StateGraph, START


from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL
from langchain.agents import create_agent

import os

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Access them using os.getenv
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

# LLM and tools
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)
tavily = TavilySearchResults(max_results=5, api_key=tavily_key)








# State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    documents: list[str]  # Text chunks
    citations: list[str]
    sufficient: bool

# Agent nodes with create_agent
def research_node(state: AgentState):
    system_prompt = "You are a Research agent. Use web search and PDFs parsing to gather data on financials/supply chain."
    research_agent = create_agent(
        llm, 
        [tavily], 
        system_prompt=system_prompt  # Specializes agent
    )
    result = research_agent.invoke({"messages": state["messages"]})
    #print("Research agent messages:", [msg.content for msg in result["messages"]])  # Debug
    new_docs = [msg.content for msg in result["messages"]]  # Extract docs
    print("Extracted documents:", new_docs)  # Debug
    return {
        "messages": [result["messages"][-1]], 
        "documents": new_docs, 
        "citations": ["Tavily results"]
    }


def review_node(state: AgentState):
    system_prompt = "You are a Critic. Check for hallucinations/gaps. Respond with 'SUFFICIENT: yes/no' and reasons."
    critic_agent = create_agent(llm, [], system_prompt=system_prompt)
    
    relevant_docs = state["documents"]  # For simplicity, use all docs
    input_msg = state["messages"] + [HumanMessage(content=f"Review docs: {relevant_docs}")]
    result = critic_agent.invoke({"messages": input_msg})
    sufficient = "yes" in result["messages"][-1].content.upper()
    return {"messages": [result["messages"][-1]], "sufficient": sufficient}

def report_node(state: AgentState):
    system_prompt = """You are a Report agent. Generate structured Markdown report: 
    # Comparison | Tesla | BYD
    Revenue: ...
    Use all documents."""
    
    report_agent = create_agent(llm, system_prompt=system_prompt)
    result = report_agent.invoke({"messages": state["messages"]})
    return {"messages": [result["messages"][-1]]}



# Graph (simplified DAG, loop via conditional)
workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("review", review_node)
workflow.add_node("report", report_node)

workflow.add_edge(START, "research")
workflow.add_edge("research", "review")
workflow.add_edge("report", END)

app = workflow.compile()

# Invoke
initial_state = {
    "messages": [HumanMessage(content="Compare Q1 2026 Tesla vs BYD financials and supply chain risks")],
    "documents": [],
    "citations": [],
    "sufficient": False
}
result = app.invoke(initial_state)
print("---------------")    
print("Final state:", result)  # Debug final state
print("---------------")   
print(result["messages"][-1].content)  # Final report