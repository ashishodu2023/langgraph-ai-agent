from typing import Dict
from langchain_core.messages import HumanMessage
from state import AgentState
from tools import calculator, search
from llm import llm
from tools import calculator, search

def classification_node(state: AgentState) -> AgentState:
    prompt = (
        f"What type of text is this (choose one: news, story, question, opinion, statement)?\n\n"
        f"Text: {state['text']}\n"
        f"Respond with only the category name."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    state["classification"] = response.content.strip().lower().split()[0]
    return state


def entity_extraction_node(state: AgentState) -> AgentState:
    prompt = (
        f"Extract only the names of entities (people, organizations, locations) "
        f"from the following text and return as a comma-separated list:\n\n{state['text']}"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    raw_entities = response.content.strip()

    # Clean and split
    entities = [e.strip().strip("*-• ") for e in raw_entities.split(",") if e.strip()]
    state["entities"] = entities
    return state

def summarization_node(state: AgentState) -> AgentState:
    prompt = f"Summarize this content in one short sentence:\n\n{state['text']}"
    response = llm.invoke([HumanMessage(content=prompt)])
    state["summary"] = response.content.strip()
    return state






def tool_use_node(state: AgentState) -> AgentState:
    if state.get("classification") == "question":
        result = search.invoke(state["text"])
        state["summary"] = f"Search result: {result}"
    elif state.get("classification") == "math":
        result = calculator.invoke(state["text"])
        state["summary"] = f"Calculator result: {result}"
    else:
        state["summary"] = "No tool used."
    return state


