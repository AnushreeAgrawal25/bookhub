from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: Optional[int] = Field(None, example=1)
    title: str = Field(..., example="Atomic Habits")
    author: str = Field(..., example="James Clear")
    year: int = Field(..., example=2018)

    class Config:
        schema_extra = {
            "example": {
                "title": "Atomic Habits",
                "author": "James Clear",
                "year": 2018
            }
        }


