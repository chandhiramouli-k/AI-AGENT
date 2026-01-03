# 🤖 Multi-Agent AI System (LangGraph + FastAPI)

An advanced agentic AI framework that uses a **Multi-Agent Orchestrator** to handle real-world tasks. The system utilizes **Llama 3.3** for reasoning, **FAISS** for document memory, and integrates with live APIs and SQL databases.

---

## 🌟 The 4 Specialized Agents

1.  **Weather Agent**: Dynamically extracts city names to fetch live weather data via OpenWeather API.
2.  **Resume/Knowledge Agent (RAG)**: Uses a Vector Store to answer questions from uploaded PDFs/TXT files; falls back to Web Search if information is missing.
3.  **Smart Scheduler**: A reasoning agent that checks weather conditions before allowing a meeting to be booked in the database.
4.  **Database Agent**: A SQL-linked agent that retrieves and displays all stored records from the local SQLite database.

---



---

## 🛠️ Tech Stack

* **Logic**: LangGraph & LangChain
* **Brain**: Llama-3.3-70b-versatile (Groq)
* **API**: FastAPI
* **Vector DB**: FAISS (with HuggingFace Embeddings)
* **Database**: SQLite
* **Search**: DuckDuckGo

---

## 🚀 Installation & Setup

### 1. Clone & Install Dependencies
Open your terminal and run:
```bash
git clone [https://github.com/your-username/agentic-ai-system.git](https://github.com/your-username/agentic-ai-system.git)
cd agentic-ai-system

pip install fastapi uvicorn python-dotenv langchain-groq langgraph \
            langchain-huggingface langchain-community pypdf faiss-cpu \
            requests duckduckgo-search
agentic_ai/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI Server & Routes
│   ├── agents.py        # LangGraph Orchestrator
│   ├── tools.py         # Weather, Search, & SQL Tools
│   ├── database.py      # SQLite Configuration
│   └── vector_store.py  # FAISS & Embedding Logic
├── .env                 # API Keys (Create this manually)
└── README.md            # Documentation

### 🏁 Final Step for You
1.  Create the `.env` file in the root folder.
2.  Add your keys.
3.  Run `python -m app.main`.
