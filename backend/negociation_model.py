from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import *
import os
import time



load_dotenv()  # take environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

prompt_instructions = f""" You are given a chat, in where 2 or more users are discussing and attempting to settle on a travel date
for their holidays. Unfortunately, they cannot come to an agreement. Therefore, you must negociate a comprimise between these
people, based on information they have provided in the chat to select a time of travel. The current time for refrence is {time.localtime()} """

async def chat_with_gemini(chat_data: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[prompt_instructions, chat_data],
        config= types.GenerateContentConfig(
            system_instruction=prompt_instructions,
            temperature=0.3
        )
    )
    print(response.text)
    llm_json: list[TravelPreference] = response.parsed
    return llm_json


    