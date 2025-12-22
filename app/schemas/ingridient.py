from datetime import datetime

from pydantic import BaseModel


class IngridientCreate(BaseModel):
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
    category_id: int


class IngridientResponse(BaseModel):
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True
