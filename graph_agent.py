# graph_agent.py

from langgraph.graph import StateGraph, END
from langgraph.types import MessagesState
from langchain_groq import ChatGroq
from tool_schema import tool_schema
import tools

import json
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# 1. Setup LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)


# 2. LLM Planner Node
def llm_planner(state: MessagesState):
    messages = state["messages"]

    response = llm.invoke(
        messages,
        tools=tool_schema,
        tool_choice="auto",
    )

    messages.append(response)

    # If tool call requested
    if hasattr(response, "tool_calls") and response.tool_calls:
        return {"messages": messages, "next": "tool_executor"}

    # Otherwise produce final response
    return {"messages": messages, "next": "final"}


# 3. Tool Execution Node
def tool_executor(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]

    tool_call = last_message.tool_calls[0]
    tool_name = tool_call["function"]["name"]
    raw_args = tool_call["function"]["arguments"]

    args = json.loads(raw_args)

    # Execute the tool
    tool_result = getattr(tools, tool_name)(**args)

    # Return tool result back to LLM
    from langchain.schema import ToolMessage
    tool_msg = ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"]
    )
    messages.append(tool_msg)

    return {"messages": messages, "next": "llm_planner"}


# 4. Final Node
def final_response(state: MessagesState):
    messages = state["messages"]
    final_msg = messages[-1]
    return final_msg.content


# 5. Build the graph
graph = StateGraph(MessagesState)

graph.add_node("llm_planner", llm_planner)
graph.add_node("tool_executor", tool_executor)
graph.add_node("final", final_response)

graph.set_entry_point("llm_planner")

# Edges
graph.add_edge("llm_planner", "tool_executor")
graph.add_edge("tool_executor", "llm_planner")

graph.add_edge("llm_planner", END, condition=lambda out: out.get("next") == "final")

app = graph.compile()
