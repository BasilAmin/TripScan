from datetime import datetime
import requests
import json

API_KEY = 'sh967490139224896692439644109194'
URL_PRICES = 'https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search'
URL_AIRPORTS = 'https://partners.api.skyscanner.net/apiservices/v3/autosuggest/flights'
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

def get_city_iata_codes(city, country):
    query_search_payload = {
        "query": {
            "market": "ES",
            "locale": "en-GB",
            "searchTerm": city,
            "includedEntityTypes": [
            "PLACE_TYPE_AIRPORT",
            ]
        }
    }

    response = requests.post(URL_AIRPORTS, headers=headers, json=query_search_payload)
    iata_codes = []

    if response.status_code == 200:
        data = response.json()
        for place in data.get("places", []):
            iata_code = place.get("iataCode")
            city_name = place.get("cityName")
            country_name = place.get("countryName")
            country_code = place.get("countryId")
            if country_code == "US":
                country_code = "USA"
            if iata_code and city in city_name and (country_name == country or country_code == country):
                iata_codes.append(iata_code)
                print(city_name, country_name, country_code)
    return iata_codes

def get_flight_price_return(origin_city, origin_country, destination_city, destination_country, travel_go_date, travel_return_date):
    res = get_flight_price(origin_city, origin_country, destination_city, destination_country, travel_go_date)
    go_price = get_flight_price(origin_city, origin_country, destination_city, destination_country, travel_go_date)
    return_price = get_flight_price(destination_city, destination_country, origin_city, origin_country, travel_return_date)

    # Check for None values before adding
    if go_price is None or return_price is None:
        print("One of the flight prices is None. Go Price:", go_price, "Return Price:", return_price)
        return None

    return go_price + return_price

def get_flight_price(origin_city: str, origin_country, destination_city, destination_country: str, travel_date: str):
    try:
        travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d')
        year = travel_date_obj.year
        month = travel_date_obj.month
        day = travel_date_obj.day
    except ValueError:
        print("Error: travel_date must be in 'YYYY-MM-DD' format.")
        return None

    iata_codes_destination = get_city_iata_codes(destination_city, destination_country)

    # Print the extracted IATA codes
    print("Destination IATA Codes:", iata_codes_destination)

    iata_codes_origin = get_city_iata_codes(origin_city, origin_country)

    print("Origin IATA Codes:", iata_codes_origin)

    cheapest_direct_price = float('inf')  # Start with a very high price for direct flights
    cheapest_price = float('inf')  # Start with a very high price for all flights
    best_origin_iata = None
    best_destination_iata = None

    for origin_iata in iata_codes_origin:
        for destination_iata in iata_codes_destination:
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

            response = requests.post(URL_PRICES, headers=headers, json=query_payload)

            if response.status_code == 200:
                data = response.json()
                # Extract the price of the cheapest flight
                try:
                    quotes = data['content']['results']['quotes']
                    for quote_key in quotes:
                        quote = quotes[quote_key]
                        price = int(quote['minPrice']['amount'])
                        print(f"Checking flights from {origin_iata} to {destination_iata} on {travel_date}. Price:", price, '€')
                        # Always check for the cheapest price regardless of directness
                        if price < cheapest_price:
                            cheapest_price = price
                            best_origin_iata = origin_iata
                            best_destination_iata = destination_iata
                
                except KeyError:
                    print("Price not found in the response.")
                    return None
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None

    return cheapest_price if cheapest_price != float('inf') else None


def query_flight_prices(json_data: str, origin_city: str, origin_country, travel_go_date: str, travel_return_date: str):
    # Parse the JSON data
    data = json.loads(json_data)
    with open('backend/data/iata.json', 'r') as file:
        iata_codes = json.load(file)
    # Initialize an array to hold the prices
    prices = [] 
    
    # Iterate over the top recommendations
    for recommendation in data['top_recommendations']:
        destination_city = recommendation['city']
        destination_country = recommendation['country']
        
        # Query the flight price
        price = get_flight_price_return(origin_city, origin_country, destination_city, destination_country, travel_go_date, travel_return_date)
        
        # Append the price to the list
        prices.append(price)
    
    return prices


if __name__ == "__main__":
    origin_city = 'Madrid'
    origin_country = 'Spain'
    travel_go_date = '2025-08-15'
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
        "city": "Paris",
        "country": "France",
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
    prices = query_flight_prices(json_data, origin_city, origin_country, travel_go_date, travel_return_date)

    # Print the results
    if prices:
        for i, price in enumerate(prices):
            if price is not None:
                print(f"The price for the flight to {json.loads(json_data)['top_recommendations'][i]['city']} is: {price}€.")
            else:
                print(f"Could not retrieve the flight price for {json.loads(json_data)['top_recommendations'][i]['city']}.")
    else:
        print("Could not retrieve any flight prices.")
