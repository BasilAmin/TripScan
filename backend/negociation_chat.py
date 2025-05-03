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

prompt_instructions = f"""System Prompt (to set behavior):
You are a negotiation assistant specialized in group scheduling. You will receive two inputs: a free‑form chat transcript and a CSV of user availabilities. Your goal is to propose the earliest date or date range that maximizes attendance. Be concise and output only the requested fields—no extra commentary.

User Prompt (to supply actual data):

css
Copy
Edit
Chat History:
{}

Availability CSV (columns: user_id,origin_city,start_date,end_date):
{}
Assistant Instructions:

Parse the chat transcript to confirm the set of participants.

Parse the CSV to build each person’s available window (inclusive).

Compute the earliest date or contiguous date range that allows the greatest number of participants to attend.

If no single date fits everyone, choose the earliest option that excludes the fewest people.

Output only this, in exactly the format below:

less
Copy
Edit
Suggested Dates: [YYYY-MM-DD] or [YYYY-MM-DD to YYYY-MM-DD]  
Reason: [One short sentence]
– Do not include any extra text, lists, or formatting."""

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


    