from langchain.tools import tool
import requests
import re

def clean_wiki_title(query: str) -> str:
    # Remove common question prefixes and punctuation
    query = re.sub(r"(what|where|when|who|is|was|the|a)\b", "", query, flags=re.I)
    query = re.sub(r"[^\w\s]", "", query)
    return query.strip().title()


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic math expression like '2+2' or '5 * (3 + 1)'."""
    try:
        return str(eval(expression))
    except Exception:
        return "Error in expression."



@tool
def search(query: str) -> str:
    """DuckDuckGo search summary."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1&skip_disambig=1"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("AbstractText"):
            return res["AbstractText"]
        for topic in res.get("RelatedTopics", []):
            if isinstance(topic, dict) and "Text" in topic:
                return topic["Text"]
        return "No relevant information found on DuckDuckGo."
    except Exception as e:
        return f"Search failed: {str(e)}"
