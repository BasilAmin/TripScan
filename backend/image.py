import requests
from fastapi import HTTPException

def get_city_image_url(city_name: str) -> str:
    """
    Fetches a random photo URL for a city using Pexels API
    Args:
        city_name (str): Name of the city to search for
    Returns:
        str: URL of the city image
    Raises:
        HTTPException: If no image is found or API request fails
    """
    try:
        # Pexels API endpoint (no key needed)
        url = f"https://api.pexels.com/v1/search?query={city_name}+city&per_page=1"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('photos'):
            raise HTTPException(
                status_code=404,
                detail=f"No images found for {city_name}"
            )
        
        return data['photos'][0]['src']['large']
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Image service unavailable: {str(e)}"
        )