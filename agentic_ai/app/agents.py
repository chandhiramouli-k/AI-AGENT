import os
from dotenv import load_dotenv

# Load .env from the root directory
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from app.tools import get_weather, verify_and_schedule, agent_knowledge_tool, get_all_meetings

# --- API KEY CHECK ---
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    print("❌ ERROR: GROQ_API_KEY is not found! Check your .env file location.")

# Using the newer, faster Llama 3.3 model
llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

def orchestrator(user_query: str):
    q = user_query.lower()
    
    # AGENT 1 & 3: Weather/Schedule
    if "weather" in q or "schedule" in q:
        try:
            # Step 1: Extract City
            prompt = f"Identify the city name in: '{user_query}'. Return ONLY the city name. If none, return 'Chennai'."
            city_res = llm.invoke([HumanMessage(content=prompt)])
            city = city_res.content.strip()
            
            if "schedule" in q:
                return verify_and_schedule(city, "2026-01-05")
            return get_weather(city)
        except Exception as e:
            return f"Agent Error (Weather/LLM): {str(e)}"

    # AGENT 4: SQL
    elif "show" in q and "meeting" in q:
        return f"Database Records: {get_all_meetings()}"
    
    # AGENT 2: Resume/Web
    else:
        return agent_knowledge_tool(user_query)

def call_agent(state: MessagesState):
    user_input = state["messages"][-1].content
    result = orchestrator(user_input)
    return {"messages": [HumanMessage(content=str(result))]}

# LangGraph Setup (Kept same)
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_agent)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)
graph = workflow.compile()