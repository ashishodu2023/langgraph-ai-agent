from agent import agent_app

print("🧠 LangGraph AI Agent (CLI mode + memory) is live.")
print("Type 'exit' to quit.\n")

# Initialize memory to track past summaries
memory = []

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    # Prepare state dictionary
    state = {
        "text": user_input,
        "memory": memory.copy()  # copy so each turn is isolated
    }

    # Invoke LangGraph agent
    result = agent_app.invoke(state)

    # Display agent output
    print("\n=== AGENT OUTPUT ===")
    print(f"Classification: {result.get('classification', 'N/A')}")
    print(f"Entities      : {result.get('entities', 'N/A')}")
    print(f"Summary       : {result.get('summary', 'N/A')}")
    print("====================\n")

    # Store this summary into memory
    if "summary" in result and result["summary"]:
        memory.append(result["summary"])
