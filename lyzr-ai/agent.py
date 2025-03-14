import os
import requests
from dotenv import load_dotenv

load_dotenv()

def chat_with_agent(user_id, agent_id, session_id, message):
    url = os.getenv("STUDIO_URL")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": os.getenv("X_API_KEY"),
    }

    data = {
        "user_id": user_id,
        "agent_id": agent_id,
        "session_id": session_id,
        "message": message,
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error chatting with agent: {e}")
        return None

def perform_analysis(session_id, message):
    user_id = "nielay18@gmail.com"
    agent_id = os.getenv("AGENT_ID")
    response = chat_with_agent(user_id, agent_id, session_id, message)
    return response