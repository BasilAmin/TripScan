from google import genai
from google.genai import types
from dotenv import load_dotenv
from .models import *
import os
import asyncio

load_dotenv()  # take environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

prompt_instructions = """
You are given a chat with different users discussing various topics related to a trip. 
Your job is to classify the following tags based on their importance for the trip. 
1.Each tag should be assigned a score from 1 to 10, where 1 represents minimal importance and 10 represents maximum importance.
The tags to score are: food, hiking, english_friendly, nightlife, culture, safety, affordability, public_transit, walkability, cleanliness, beaches, city_cluster.
2.Include an optional "veto" field: a list of cities that the user explicitly states they do not want to visit. If no cities are vetoed, return an empty list for "veto".
3.Include an optional "favoured_city" field: a list of cities that the user explicitly states they want to visit. If no cities are favoured, return an empty list for "favoured_city".
"""

async def chat_with_gemini(chat_data: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[prompt_instructions, chat_data],
        config= types.GenerateContentConfig(
            response_mime_type= "application/json",
            response_schema = list[TravelPreference],
            system_instruction=prompt_instructions,
            temperature=0.3
        )
    )
    print(response.text)
    # Use instantiated objects.
    llm_json: list[TravelPreference] = response.parsed
    return llm_json

if __name__ == "__main__":
    chat_example = """
    User1: I love hiking and exploring nature.
    User2: I prefer relaxing on the beach and enjoying the sun.
    User3: I enjoy trying out local cuisines and visiting historical sites.
    User4: I like adventure sports and thrilling activities.
    User5: I am interested in cultural experiences and art galleries.
    """
    asyncio.run(chat_with_gemini(chat_example))
    