import os
import sys
import requests

API_KEY = os.getenv("FOURSQUARE_API_KEY")
if not API_KEY:
    print("Error: set FOURSQUARE_API_KEY in your environment")
    sys.exit(1)

HEADERS = {
    "Accept": "application/json",
    "Authorization": API_KEY
}

def fetch_hotels(city: str, limit: int = 5):
    """
    Search for hotels in the given city.
    Returns a list of place dicts from Foursquare.
    """
    resp = requests.get(
        "https://api.foursquare.com/v3/places/search",
        headers=HEADERS,
        params={
            "query": "hotel",
            "near": city,
            "limit": limit
        }
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

def fetch_photo_url(fsq_id: str):
    """
    Fetch the first photo for a given place ID.
    """
    resp = requests.get(
        f"https://api.foursquare.com/v3/places/{fsq_id}/photos",
        headers=HEADERS,
        params={"limit": 1}
    )
    resp.raise_for_status()
    photos = resp.json()
    if photos:
        p = photos[0]

        return f"{p['prefix']}original{p['suffix']}"
    return None

def display_hotels(city: str):
    hotels = fetch_hotels(city)
    if not hotels:
        print(f"No hotels found for '{city}'.")
        return

    for i, h in enumerate(hotels, 1):
        name = h.get("name", "–")
        loc = ", ".join(h.get("location", {}).get("formatted_address", []))
        photo = fetch_photo_url(h["fsq_id"]) or "No image"
        print(f"{i}. {name}")
        print(f"   Location: {loc}")
        print(f"   Photo:    {photo}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hotel_info_fsq.py <CityName>")
        sys.exit(1)
    display_hotels(sys.argv[1])
