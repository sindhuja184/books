from pydantic import BaseModel
from typing import List

class RecommendationResponse(BaseModel):
    book_uid: str
    recommendations: List[str]
