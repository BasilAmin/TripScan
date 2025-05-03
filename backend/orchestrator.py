from .messages import *
from .chat import *
import asyncio

async def main_process():    
    llm_message = get_llm_formatted_input(messages_file="messages.csv", trips_file="trips.csv")
    llm_json = await chat_with_gemini(llm_message)

