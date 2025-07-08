from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import (
    classification_node,
    entity_extraction_node,
    summarization_node,
    tool_use_node,
    rewrite_query_node
)

#  Initialize the graph builder
builder = StateGraph(AgentState)

def router(state: AgentState) -> str:
    return "rewrite_query" if state.get("classification") == "question" else "extract_entities"


                            
#  Register nodes
builder.add_node("classify", classification_node)
builder.add_node("rewrite_query", rewrite_query_node)
builder.add_node("tool_use", tool_use_node)
builder.add_node("extract_entities", entity_extraction_node)
builder.add_node("summarize", summarization_node)

#  Entry point
builder.set_entry_point("classify")

#  Conditional path from classify → question → rewrite → tool
#                          or   → other → extract → summarize
def router(state: AgentState) -> str:
    if state.get("classification", "") == "question":
        return "rewrite_query"
    else:
        return "extract_entities"

builder.add_conditional_edges(
    "classify",
    router,
    {
        "rewrite_query": "rewrite_query",
        "extract_entities": "extract_entities"
    }
)

# 🔗 Connect rest of the flow
builder.add_edge("rewrite_query", "tool_use")
builder.add_edge("tool_use", END)

builder.add_edge("extract_entities", "summarize")
builder.add_edge("summarize", END)

# Compile the graph into an app
agent_app = builder.compile()

# Optional: visualize
print("Saved: langgraph_workflow.png")

from graphviz import Digraph

def export_langgraph_png():
    dot = Digraph(comment="LangGraph AI Workflow")

    dot.node("C", "classify")
    dot.node("R", "rewrite_query")
    dot.node("T", "tool_use")
    dot.node("E", "extract_entities")
    dot.node("S", "summarize")
    dot.node("END", "END")

    dot.edge("C", "R", label="if question")
    dot.edge("C", "E", label="else")
    dot.edge("R", "T")
    dot.edge("E", "S")
    dot.edge("S", "END")
    dot.edge("T", "END")

    dot.render("langgraph_workflow", format="png", cleanup=True)

export_langgraph_png()
