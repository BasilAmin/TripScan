from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    tag: str
    score: int

class TravelPreference(BaseModel):
    user: str
    tags: List[Tag]

class Message(BaseModel):
    user_id: str
    content: str

class TripData(BaseModel):
    origin_city: str  # Three-letter city code
    start_date: str   # Start date in ISO format (YYYY-MM-DD)
    end_date: str     # End date in ISO format (YYYY-MM-DD)