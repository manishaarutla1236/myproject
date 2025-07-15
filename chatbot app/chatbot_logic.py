# chatbot_logic.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_bot_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"
