from agent import agent_app

print(" AI Agent is live. Type 'exit' to quit.")

while True:
    user_input = input("Enter text: ")
    if user_input.lower() == "exit":
        break

    result = agent_app.invoke({"text": user_input})
    print("\n=== AGENT OUTPUT ===")
    print(f"Classification: {result.get('classification', 'N/A')}")
    print(f"Entities      : {result.get('entities', 'N/A')}")
    print(f"Summary       : {result.get('summary', '')}")

