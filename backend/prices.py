from datetime import datetime
import requests
import json

API_KEY = 'sh967490139224896692439644109194'
URL = 'https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search'

def get_flight_price_return(origin_iata: str, destination_iata: str, travel_go_date: str, travel_return_date: str):
    return get_flight_price(origin_iata, destination_iata, travel_go_date) + get_flight_price(origin_iata, destination_iata, travel_return_date)

def get_flight_price(origin_iata: str, destination_iata: str, travel_date: str):
    try:
        travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d')
        year = travel_date_obj.year
        month = travel_date_obj.month
        day = travel_date_obj.day
    except ValueError:
        print("Error: travel_date must be in 'YYYY-MM-DD' format.")
        return None
    
    query_payload = {
        "query": {
            "market": "ES",
            "locale": "en-GB",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlace": {
                        "queryPlace": {
                            "iata": origin_iata
                        }
                    },
                    "destinationPlace": {
                        "queryPlace": {
                            "iata": destination_iata
                        }
                    },
                    "fixedDate": {
                        "year": year,
                        "month": month,
                        "day": day
                    },
                }
            ],
            "dateTimeGroupingType": "DATE_TIME_GROUPING_TYPE_UNSPECIFIED"
        }
    }

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }

    response = requests.post(URL, headers=headers, json=query_payload)

    if response.status_code == 200:
        data = response.json()
        # Extract the price of the cheapest direct flight
        try:
            quotes = data['content']['results']['quotes']
            cheapest_direct_price = float('inf')  # Start with a very high price for direct flights
            cheapest_price = float('inf')  # Start with a very high price for all flights
            
            for quote_key in quotes:
                quote = quotes[quote_key]
                price = int(quote['minPrice']['amount'])
                
                if quote['isDirect']:  # Check if the flight is direct
                    if price < cheapest_direct_price:  # Find the minimum direct price
                        cheapest_direct_price = price
                # Always check for the cheapest price regardless of directness
                if price < cheapest_price:
                    cheapest_price = price
            return cheapest_price
        except KeyError:
            print("Price not found in the response.")
            return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None


def query_flight_prices(json_data: str, origin_iata: str, travel_go_date: str, travel_return_date: str):
    # Parse the JSON data
    data = json.loads(json_data)
    with open('backend/data/iata.json', 'r') as file:
        iata_codes = json.load(file)
    # Initialize an array to hold the prices
    prices = [] 
    
    # Iterate over the top recommendations
    for recommendation in data['top_recommendations']:
        city = recommendation['city']
        country = recommendation['country']
        
        # Here you would need to determine the destination IATA code based on the city and country
        destination_iata = iata_codes[city]  # You need to implement this function
        
        # Query the flight price
        price = get_flight_price_return(origin_iata, destination_iata, travel_go_date, travel_return_date)
        
        # Append the price to the list
        prices.append(price)
    
    return prices


if __name__ == "__main__":
    origin = 'MAD'  # Example IATA code for New York
    travel_go_date = '2025-08-15'  # Example travel date
    travel_return_date = '2025-09-15'

    json_data = '''{
    "aggregate_preferences": {
        "hiking": 0.07245898866903433,
        "food": 0.09703619144258413,
        "nightlife": 0.053014544224589885,
        "safety": 0.10830373752748182,
        "culture": 0.09896414679519702,
        "beaches": 0.061466260781329274,
        "walkability": 0.09182732961271774,
        "public_transit": 0.070645188567563,
        "cleanliness": 0.10004650769490953,
        "affordability": 0.08137155420260442,
        "english_friendly": 0.08658041603247082
    },
    "top_recommendations": [
        {
        "city": "New York",
        "country": "USA",
        "match_score": 44.0,
        "features": {
            "hiking": 4.0,
            "food": 10.0,
            "nightlife": 10.0,
            "safety": 10.0,
            "culture": 5.0,
            "beaches": 8.0,
            "walkability": 3.0,
            "public_transit": 6.0,
            "cleanliness": 7.0,
            "affordability": 7.0,
            "english_friendly": 4.0
        }
        },
        {
        "city": "Barcelona",
        "country": "Spain",
        "match_score": 37.7,
        "features": {
            "hiking": 1.0,
            "food": 4.0,
            "nightlife": 6.0,
            "safety": 1.0,
            "culture": 2.0,
            "beaches": 2.0,
            "walkability": 7.0,
            "public_transit": 5.0,
            "cleanliness": 4.0,
            "affordability": 3.0,
            "english_friendly": 6.0
        }
        },
        {
        "city": "Tokyo",
        "country": "Japan",
        "match_score": 18.3,
        "features": {
            "hiking": 7.0,
            "food": 2.0,
            "nightlife": 6.0,
            "safety": 6.0,
            "culture": 7.0,
            "beaches": 3.0,
            "walkability": 1.0,
            "public_transit": 6.0,
            "cleanliness": 7.0,
            "affordability": 1.0,
            "english_friendly": 4.0
        }
        }
    ]
    }'''
    # Call the query_flight_prices function
    prices = query_flight_prices(json_data, origin, travel_go_date, travel_return_date)

    # Print the results
    if prices:
        for i, price in enumerate(prices):
            if price is not None:
                print(f"The price for the flight to {json.loads(json_data)['top_recommendations'][i]['city']} is: {price}€.")
            else:
                print(f"Could not retrieve the flight price for {json.loads(json_data)['top_recommendations'][i]['city']}.")
    else:
        print("Could not retrieve any flight prices.")
