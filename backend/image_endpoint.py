from fastapi import APIRouter, HTTPException
from .image import get_city_image_url

router = APIRouter()

@router.get("/city-image/{city_name}")
async def get_city_image(city_name: str):
    """
    Endpoint to get an image URL for a city
    """
    try:
        image_url = get_city_image_url(city_name)
        return {"city": city_name, "image_url": image_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))