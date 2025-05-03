import requests

def get_city_image_link(city_name):
    """
    Fetches a random photo link of the specified city using Pexels API.
    No API key required.    Args:
        city_name (str): Name of the city to search for    Returns:
        str: Direct URL to a city image or error message
    """
    try:
        # Pexels API endpoint (no key needed)
        url = f"https://api.pexels.com/v1/search?query={city_name}+city+skyline&per_page=1"        # Make the request with default headers
        headers = {
            "Authorization": "uf8L1WVvEn7L6obVPlw8JZv1VXE6LkVTegXKbZeJAsx5vFCGMIEcBqRL"
        }
        # Make the request with the headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data.get('photos'):
            return f"No images found for {city_name}"
        print(data['photos'][0]['src']['large'])
        return(data['photos'][0]['src']['large'])
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching image: {str(e)}"# Example usage

if __name__ == "__main__":
    city = input().strip()
    if not city:
        print("Please enter a valid city name")
    else:
        image_link = get_city_image_link(city)
        print("\nImage Link:", image_link)