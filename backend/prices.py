from datetime import datetime
import requests
import json
from .messages import *
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SKYSCANNER_API_KEY")

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
    return iata_codes

def get_flight_price(origin_city: str, origin_country: str, destination_city: str, destination_country: str, travel_date: str):
    try:
        travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d')
        year = travel_date_obj.year
        month = travel_date_obj.month
        day = travel_date_obj.day
    except ValueError:
        print("Error: travel_date must be in 'YYYY-MM-DD' format.")
        return None

    # Get IATA codes for the origin and destination cities
    iata_codes_destination = get_city_iata_codes(destination_city, destination_country)
    iata_codes_origin = get_city_iata_codes(origin_city, origin_country)

    cheapest_price = float('inf')

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

                # Extract quotes and carriers
                quotes = data['content']['results']['quotes']
                carriers = data['content']['results']['carriers']
                places = data['content']['results']['places']

                for quote_key, quote in quotes.items():
                    price = int(quote['minPrice']['amount'])
                    is_direct = quote['isDirect']
                    outbound_leg = quote['outboundLeg']
                    inbound_leg = quote['inboundLeg']

                    # Extract relevant details
                    departure_time = outbound_leg['departureDateTime']  # assuming outbound leg for departure time
                    origin_place_id = outbound_leg['originPlaceId']
                    destination_place_id = outbound_leg['destinationPlaceId']

                    origin = places[str(origin_place_id)]['name']
                    destination = places[str(destination_place_id)]['name']

                    # Get airline information
                    carrier_id = outbound_leg['marketingCarrierId']
                    airline = carriers[str(carrier_id)]['name']

                    formatted_date = format_flight_date(departure_time)

                    # Always check for the cheapest price
                    if price < cheapest_price:
                        cheapest_price = price
                        flight_info = {
                            'departure_time': departure_time,
                            'origin': origin,
                            'destination': destination,
                            'airline': airline,
                            'price': price,
                            'is_direct': is_direct
                        }
                
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None

    return flight_info if flight_info else None

def format_flight_date(flight_date: dict):
    # Extract the components from the dictionary
    year = flight_date['year']
    month = flight_date['month']
    day = flight_date['day']
    hour = flight_date['hour']
    minute = flight_date['minute']
    second = flight_date['second']

    # Create a datetime object from the components
    flight_datetime = datetime(year, month, day, hour, minute, second)

    # Format the date to only show day, hour, and minute
    formatted_date = flight_datetime.strftime('%d %H:%M')

    return formatted_date

def skyscanner_api_request(user_id, destination_city):
    # Load the JSON data from the file
    with open("output.json", "r", encoding="utf-8") as f:  # Ensure the filename matches your actual file
        json_data = json.load(f)
    
    for recommendation in json_data.get("top_recommendations", []):
        if recommendation.get("city") == destination_city:
            destination_country = recommendation.get("country")
            
    trips = load_trip_data_from_csv('trips.csv')

    # Find the trip for the specified user_id
    trip = next((t for t in trips if t.user_id == user_id), None)
    
    if not trip:
        print(f"No trip found for user {user_id}")
        return []

    # Extract trip details
    origin_city = trip.origin_city
    origin_country = trip.origin_country
    start_date = trip.start_date
    end_date = trip.end_date

    with open('backend/data/iata.json', 'r') as file:
        iata_codes = json.load(file)
    
    # Vuelos de ida
    info_fligh1 = get_flight_price(origin_city, origin_country, destination_city, destination_country, start_date)

    # Vuelos de vuelta
    info_fligh2 = get_flight_price(destination_city, destination_country, origin_city, origin_country, end_date)

    # Add botwh flight info to the JSON data
    if info_fligh1 and info_fligh2:
        json_data['flight_info'] = {
            "outbound": {
                "departure_time": info_fligh1['departure_time'],
                "origin": info_fligh1['origin'],
                "destination": info_fligh1['destination'],
                "airline": info_fligh1['airline'],
                "price": info_fligh1['price']
            },
            "inbound": {
                "departure_time": format_flight_date,
                "origin": info_fligh2['origin'],
                "destination": info_fligh2['destination'],
                "airline": info_fligh2['airline'],
                "price": info_fligh2['price']
            }
        }
    
    return json_data['flight_info']

