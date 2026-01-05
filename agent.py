import os
from typing import Literal
from dotenv import load_dotenv

# 1. Necessary Imports
from langchain_core.messages import SystemMessage  # Essential for tool-use instructions
from langchain_groq import ChatGroq 
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode
from tools import query_customer_info, search_knowledge_base, get_external_info

# Load environment variables from .env
load_dotenv()

# 2. Setup the tools
tools = [query_customer_info, search_knowledge_base, get_external_info]

# 3. Initialize the current Groq Model
model = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
# Bind tools so the model knows their schemas
model_with_tools = model.bind_tools(tools)

# 4. Define the Routing Logic
def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]
    # Check if the model generated tool calls
    if last_message.tool_calls:
        return "tools"
    return "__end__"

# 5. Define the Node that calls the model with instructions
def call_model(state: MessagesState):
    messages = state['messages']
    
    # Forceful identity: Tell the AI it is REQUIRED to use tools
    system_prompt = SystemMessage(content=(
        "You are a helpful AI Support Assistant. "
        "You HAVE access to a PostgreSQL database for customer info and a "
        "ChromaDB for knowledge base articles. "
        "Always use your tools to find information. "
        "If a user asks about a person like 'Alice', you MUST call 'query_customer_info' "
        "to search the database. Do not say you don't have access."
    ))
    
    # Important: Create the message list with System Prompt at the start
    input_messages = [system_prompt] + messages
    
    # Invoke the model
    response = model_with_tools.invoke(input_messages)
    
    # Return as a list to update the MessagesState
    return {"messages": [response]}

# 6. Build the Graph
workflow = StateGraph(MessagesState)

# Add Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Define Edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent") # Cycle back to summarize tool results

# Compile the Graph
app = workflow.compile()