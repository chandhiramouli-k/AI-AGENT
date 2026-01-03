import os
import requests
from app.database import add_meeting, get_all_meetings
from app.vector_store import query_document
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

def get_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY is missing from environment."
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The weather in {city} is {temp}°C with {desc}."
        elif response.status_code == 401:
            return "Error: Invalid OpenWeather API Key."
        else:
            return f"Error: OpenWeather API returned {data.get('message', 'Unknown Error')}"
    except Exception as e:
        return f"Weather Tool Connection Error: {str(e)}"

def verify_and_schedule(city: str, date: str):
    weather_report = get_weather(city)
    # If there's an error message in weather, don't schedule
    if "Error" in weather_report:
        return f"Cannot schedule. {weather_report}"
    
    if "rain" in weather_report.lower():
        return f"Rejected: It is raining in {city}. Let's stay home!"
    
    add_meeting("AI Project Sync", date, f"Weather in {city}: Clear")
    return f"Success! Meeting booked for {date} in {city}."

def agent_knowledge_tool(query: str):
    res = query_document(query)
    if res:
        return res
    return search_tool.run(query)