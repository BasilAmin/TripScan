from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

my_file = client.files.upload(file="image.jpg")

# Instruct Gemini to identify the place in the image
prompt_instructions = """
You are a geolocation assistant. 
Analyze the image and return the most likely city, based solely on visual cues.
Do not return anything else, simply these two things
"""

async def image_to_location():
    # Call a vision-capable Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt_instructions, my_file],
        config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            temperature=0.0
        )
    )
    print("Response from Gemini:")
    print(response.text)
    # Strip and return the plain-text location
    return response.text.strip()

def save_image_to_file(base64_str: str):
    # Decode the base64 string and save the image to a file
    try:
        image_data = base64.b64decode(base64_str.split(",")[1])  # Handle potential prefix like "data:image/jpeg;base64,"
        with open("uploaded_image.jpg", "wb") as f:
            f.write(image_data)
    except Exception as e:
        return f"Error saving image: {e}"
        
        
if __name__ == "__main__":
    asyncio.run(image_to_location())
