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
    prompt = (
        f"Previous context: {state.get('memory', [])}\n\n"
        f"Summarize this new input:\n\n{state['text']}"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    state["summary"] = response.content.strip()
    return state


def tool_use_node(state: AgentState) -> AgentState:
    query = state.get("rewritten_query", "").strip() or state["text"].strip()
    print("[Using Query]:", query)

    result = search.invoke(query)
    state["summary"] = f"Search result: {result}"
    return state



def rewrite_query_node(state: AgentState) -> AgentState:
    prompt = (
        f"You are a web search assistant.\n"
        f"Your job is to take the user’s question and turn it into a short, keyword-based Google-style search query.\n\n"
        f"QUESTION:\n{state['text']}\n\n"
        f"ONLY output the rewritten query — no explanation, no quotes, no formatting. Just the keywords."
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    rewritten = response.content.strip()

    print("[Rewritten Query]:", rewritten)

    return {
        **state,
        "rewritten_query": rewritten
    }
