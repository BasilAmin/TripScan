from google import genai
from google.genai import types
from dotenv import load_dotenv
from .models import *
import os
import time
import re

load_dotenv()  # take environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

prompt_instructions = f""" You are given a chat, in where 2 or more users are discussing and attempting to settle on a travel date
for their holidays. Unfortunately, they cannot come to an agreement. Therefore, you must negociate a comprimise between these
people, based on information they have provided in the chat to select a time of travel. The current time for refrence is {time.localtime()} 
Provide short and concise answers, and do not include any unnecessary information."""

async def negociate_with_gemini(chat_data: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[prompt_instructions, chat_data],
        config= types.GenerateContentConfig(
            system_instruction=prompt_instructions,
            temperature=0.3
        )
    )
    print("Text provided:")
    print(chat_data)
    cleaned_text = re.sub(r'\*+', '', response.text)  # removes *, **, ***
    print(cleaned_text)
    return cleaned_text


    