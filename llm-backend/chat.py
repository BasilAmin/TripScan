from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import TravelPreference
import os
import asyncio

load_dotenv()  # take environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

prompt_instructions = """
You are given a chat with different users discussing various topics related to a trip. 
Your job is to classify different tags based on their importance for the trip. 
Each tag should be assigned a score from 1 to 10, where 1 represents minimal importance and 10 represents maximum importance."""

chat_data = """
User1: I love hiking and exploring nature.
User2: I prefer relaxing on the beach and enjoying the sun.
User3: I enjoy trying out local cuisines and visiting historical sites.
User4: I like adventure sports and thrilling activities.
User5: I am interested in cultural experiences and art galleries.
"""

async def chat_with_gemini():
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[prompt_instructions, chat_data],
        config= types.GenerateContentConfig(
            response_mime_type= "application/json",
            response_schema = list[TravelPreference],
            system_instruction=prompt_instructions,
            temperature=0.3,
            max_output_tokens=1000,
        )
    )
    print(response.text)
    return response.text

if __name__ == "__main__":
    asyncio.run(chat_with_gemini())