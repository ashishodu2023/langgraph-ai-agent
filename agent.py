from nodes import classification_node, entity_extraction_node, summarization_node, tool_use_node
from langgraph.graph import StateGraph, END
from state import AgentState
from graphviz import Digraph


# Initialize graph
builder = StateGraph(AgentState)

# Nodes
builder.add_node("classify", classification_node)
builder.add_node("extract_entities", entity_extraction_node)
builder.add_node("summarize", summarization_node)
builder.add_node("tool_use", tool_use_node)

# Entry
builder.set_entry_point("classify")

# Conditional branching based on classification
def router(state: AgentState) -> str:
    if state.get("classification") == "question":
        return "tool_use"
    else:
        return "extract_entities"

builder.add_conditional_edges(
    "classify",
    router,
    {
        "tool_use": "tool_use",
        "extract_entities": "extract_entities"
    }
)

def export_langgraph_png():
    dot = Digraph(comment="LangGraph Workflow")

    dot.node("C", "classify")
    dot.node("T", "tool_use")
    dot.node("E", "extract_entities")
    dot.node("S", "summarize")
    dot.node("END", "END")

    # Conditional path from classification
    dot.edge("C", "T", label="if question")
    dot.edge("C", "E", label="else")

    # Regular flow
    dot.edge("E", "S")
    dot.edge("S", "END")
    dot.edge("T", "END")

    dot.render("langgraph_workflow", format="png", cleanup=True)
    print("✅ Saved: langgraph_workflow.png")

export_langgraph_png()


# Complete the branches
builder.add_edge("tool_use", END)
builder.add_edge("extract_entities", "summarize")
builder.add_edge("summarize", END)

# Compile
agent_app = builder.compile()
