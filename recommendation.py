from .messages import *
from .chat import *
import asyncio
import json
from typing import List, Optional
from .models import TravelPreference  # Import the model for type hints

async def main_process():    
    # Step 1: Get formatted input from CSV files (unchanged)
    llm_message = get_llm_formatted_input(messages_file="messages.csv", trips_file="trips.csv")
    
    # Step 2: Get JSON response from Gemini (unchanged)
    llm_json: List[TravelPreference] = await chat_with_gemini(llm_message)
    
    # Step 3: Save the JSON output to location.json with optional veto handling
    output_data = []
    for pref in llm_json:
        pref_dict = pref.dict()
        # Add empty veto field if not present
        if 'veto' not in pref_dict:
            pref_dict['veto'] = []  # or None if you prefer
        output_data.append(pref_dict)
    
    with open('location.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    # Step 4: Call the recommendation script (unchanged)
    try:
        import recommendation
        recommendations = recommendation.generate_recommendations('location.json')
        print("Recommendations generated successfully")
        return recommendations
    except ImportError:
        print("Error: recommendation.py not found")
        return None
    except Exception as e:
        print(f"Error running recommendation script: {e}")
        return None

# Run the main process (unchanged)
if __name__ == "__main__":
    asyncio.run(main_process())