from datetime import datetime
import requests
import json

API_KEY = 'sh967490139224896692439644109194'
URL = 'https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search'  # Example endpoint

def get_flight_price(api_key: str, origin_iata: str, destination_iata: str, travel_date: str):
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
        'x-api-key': api_key
    }

    response = requests.post(URL, headers=headers, json=query_payload)

    if response.status_code == 200:
        data = response.json()
        # Extract the price of the cheapest direct flight
        try:
            quotes = data['content']['results']['quotes']
            cheapest_price = float('inf')  # Start with a very high price
            for quote_key in quotes:
                quote = quotes[quote_key]
                if quote['isDirect']:  # Check if the flight is direct
                    price = int(quote['minPrice']['amount'])
                    if price < cheapest_price:  # Find the minimum price
                        cheapest_price = price
            
            if cheapest_price == float('inf'):
                print("No direct flights found.")
                return None
            
            return cheapest_price
        except KeyError:
            print("Price not found in the response.")
            return None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None


if __name__ == "__main__":
    origin = 'JFK'  # Example IATA code for New York
    destination = 'BCN'  # Example IATA code for Los Angeles
    travel_date = '2025-08-15'  # Example travel date

    price = get_flight_price(API_KEY, origin, destination, travel_date)
    if price is not None:
        print(f"The price for the flight is: {price}€.")
    else:
        print("Could not retrieve the flight price.")
