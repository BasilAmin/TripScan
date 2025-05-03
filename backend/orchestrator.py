from .messages import *
from .chat import *
from .negociation_chat import *
import asyncio
import json
from .prices import *
from typing import List
from .models import TravelPreference  # Import the model for type hints
from .recommendation import RobustCityRecommender, generate_recommendations  # Import the recommender class

async def main_process():
    # Step 1: Get formatted input from CSV files
    llm_message = get_llm_formatted_chat(messages_file="messages.csv")
    
    # Step 2: Get JSON response from Gemini
    llm_json: List[TravelPreference] = await chat_with_gemini(llm_message)
    
    # Save the JSON response to a file for debugging
    llm_json_dict = [pref.dict() for pref in llm_json]
    with open('llm_response.json', 'w') as f:
            json.dump(llm_json_dict, f, indent=2)

    # Step 3: Call the recommendation script
    try:
        recommendations = generate_recommendations(llm_json)
        print("Recommendations generated successfully:")
        print(recommendations)

        #Step 4: Let the user know the recommendations
        save_message_to_csv("System", "The recommendations are ready. Please click the b the output.json file.")
    except ImportError:
        print("Error: recommendation.py not found")
    except Exception as e:
        print(f"Error running recommendation script: {e}")
    """
    # Step 4: Calling SkyScanner API
    with open('recommendation/output.json', 'r') as recommendation_output:
        json_data = json.loads(recommendation_output)
    prices = query_flight_prices(json_data, origin_city, origin_country, travel_go_date, travel_return_date)
    # Insert the 'price' attribute into each city
    i = 0
    for city in json_data['cities']:
        city = prices[i]
        i += 1
    with open('output_price.json', 'w') as json_file:
        json_file.write(json_data)"""

async def negociation_process():
    try:
        # Step 1: Get formatted input from CSV files
        llm_message = get_llm_formatted_date(trips_file="trips.csv")
        
        # Step 2: Get JSON response from Gemini
        llm_response = await negociate_with_gemini(llm_message)

        save_message_to_csv("System", llm_response)
        
    except ImportError:
        print("Error: recommendation.py not found")
    except Exception as e:
        print(f"Error running recommendation script: {e}")

def priceJSONTest():
    origin_city = 'Madrid'
    origin_country = 'Spain'
    travel_go_date = '2025-08-15'
    travel_return_date = '2025-09-15'
    with open('recommendation/output.json', 'r') as recommendation_output:
        json_data = json.load(recommendation_output)

    prices = query_flight_prices(json_data, origin_city, origin_country, travel_go_date, travel_return_date)
    # Insert the 'price' attribute into each city
    for i, city in enumerate(json_data['top_recommendations']):
        city['price'] = prices[i]  # Assign the price to the city

    with open('output_price.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    if prices:
        for i, price in enumerate(prices):
            if price is not None:
                print(f"The price for the flight to {json_data['top_recommendations'][i]['city']} is: {price}€.")
            else:
                print(f"Could not retrieve the flight price for {json_data['top_recommendations'][i]['city']}.")
    else:
        print("Could not retrieve any flight prices.")


# Run the main process
if __name__ == "__main__":
    asyncio.run(main_process())