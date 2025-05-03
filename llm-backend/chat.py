from google import genai
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

async def chat_with_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works in a few words"
    )
    print(response.text)
    return response.text