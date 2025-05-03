from .messages import *
from .chat import *
import asyncio
import json
from typing import List
from .models import TravelPreference  # Import the model for type hints

async def main_process():
    # Step 1: Get formatted input from CSV files
    llm_message = get_llm_formatted_input(messages_file="messages.csv", trips_file="trips.csv")
    
    # Step 2: Get JSON response from Gemini
    llm_json: List[TravelPreference] = await chat_with_gemini(llm_message)
    
    # Step 3: Save the JSON output to input.json
    with open('input.json', 'w') as f:
        # Convert Pydantic models to dict first
        json.dump([pref.dict() for pref in llm_json], f, indent=2)
    
    # Step 4: Call the recommendation script
    try:
        import recommendation  # Assuming recommendation.py is in the same directory
        recommendations = recommendation.generate_recommendations('input.json')
        print("Recommendations generated successfully:")
        print(recommendations)
    except ImportError:
        print("Error: recommendation.py not found")
    except Exception as e:
        print(f"Error running recommendation script: {e}")

# Run the main process
if __name__ == "__main__":
    asyncio.run(main_process())