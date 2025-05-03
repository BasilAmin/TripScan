from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    tag: str
    score: int

class TravelPreference(BaseModel):
    user: str
    tags: List[Tag]