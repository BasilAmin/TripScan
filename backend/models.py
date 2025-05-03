from pydantic import BaseModel
from typing import List, Optional

class Tag(BaseModel):
    tag: str
    score: int

class TravelPreference(BaseModel):
    user: str
    tags: List[Tag]
    veto: Optional[List[str]] = []

class Message(BaseModel):
    user_id: str
    content: str

class TripData(BaseModel):
    user_id: str
    origin_city: str  # Three-letter city code
    start_date: str   # Start date in ISO format (YYYY-MM-DD)
    end_date: str     # End date in ISO format (YYYY-MM-DD)

class MessageImage(BaseModel):
    user_id: str
    content: str = ""
    image: str = ""  # Base64 string