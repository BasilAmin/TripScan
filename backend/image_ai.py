from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Instruct Gemini to identify the place in the image
prompt_instructions = """
You are a geolocation assistant. 
Analyze the image and return the most likely city and country depicted, based solely on visual cues.
Do not return anything else, simply these two things
"""

async def image_to_location(image_path: str) -> str:
    # Load image bytes
    with open(image_path, "rb") as img_f:
        img_bytes = img_f.read()

    # Wrap in Gemini's ImageInput
    image_input = types.ImageInput(
        data=img_bytes,
        mime_type="image/jpeg"  # or "image/png"
    )

    # Call a vision-capable Gemini model
    response = await client.models.generate_content(
        model="gemini-2.0-vision",
        contents=[prompt_instructions, image_input],
        config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            temperature=0.0
        )
    )

    # Strip and return the plain-text location
    return response.text.strip()

if __name__ == "__main__":
    img_path = "path/to/city_image.jpg"
    location = asyncio.run(image_to_location(img_path))
    print("Detected location:", location)
