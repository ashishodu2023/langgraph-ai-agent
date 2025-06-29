from langchain.tools import tool
import requests

@tool
def calculator(expression: str) -> str:
    """Evaluate a basic math expression like '2+2' or '5 * (3 + 1)'."""
    try:
        return str(eval(expression))
    except Exception:
        return "Error in expression."



@tool
def search(query: str) -> str:
    """Search Wikipedia for a summary of the query."""
    try:
        title = query.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No summary available.")
        elif response.status_code == 404:
            return "No Wikipedia page found."
        else:
            return f"Search failed with status: {response.status_code}"
    except Exception as e:
        return f"Search error: {str(e)}"