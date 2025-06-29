# 🧠 LangGraph AI Agent (Groq + Wikipedia)

This project implements an AI reasoning agent using [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://www.langchain.com/) with **Groq’s blazing-fast LLaMA3 model**.

The agent:
- Classifies text as a question, fact, story, etc.
- Branches the workflow using LangGraph based on classification
- Uses tools like Wikipedia search and math calculator
- Summarizes and tracks key information across nodes
- Is deployable in both CLI and Streamlit UI

---

## 🚀 Features

- ✅ LangGraph-based multi-node agent (classification → tool use → summary)
- 🤖 LLaMA3 (via Groq) for low-latency language understanding
- 🔍 Wikipedia integration for fast question answering
- 🧮 Calculator for math queries
- 🧠 TypedDict-based state memory
- 📦 Visual PNG diagram of agent workflow
- 💻 CLI and Streamlit interface
- 📝 Session memory + logging

---

## 📁 Project Structure

ai_agent_project/
├── .env # API keys for Groq, etc.
├── agent.py # LangGraph definition & logic
├── nodes.py # All LangGraph node functions
├── tools.py # Search (Wikipedia) + calculator
├── state.py # AgentState (TypedDict)
├── llm.py # Groq LLaMA3 setup
├── main.py # CLI interface
├── app.py # Streamlit web app
├── requirements.txt # All dependencies
├── langgraph_workflow.png # Visual graph of agent
└── README.md # You're here

```yaml

---

## 🌐 How It Works

1. **User Input** → passed to LangGraph.
2. **Classification Node** → determines type of text.
3. **Branching**:
   - If **question** → → Wikipedia tool
   - Else → Entity Extraction → Summarization
4. **Summary & Output** → returned with classification + entities.

---

## 🧪 Example Output

```bash
Enter text: What is the capital of India?

=== AGENT OUTPUT ===
Classification: question
Entities      : N/A
Summary       : New Delhi is the capital of India.
```

* Clone the repo
```bash 
git clone https://github.com/your-username/langgraph-ai-agent.git
cd langgraph-ai-agent
```

* Create a virtual environment
```bash 
python3 -m venv agent_env
source agent_env/bin/activate
```
* Install dependencies
```bash 
pip install -r requirements.txt
```

* Add your .env file
```bash
GROQ_API_KEY=your_groq_api_key_here
```

* Run Agent
```bash
python main.py
```
