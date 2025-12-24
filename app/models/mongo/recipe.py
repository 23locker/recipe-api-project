from datetime import datetime
from multiprocessing.managers import BaseManager
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        json_schema = super().__get_pydantic_json_schema__(schema)
        json_schema = {"type": "string"}
        return json_schema


class RecipeIngredient(BaseModel):
    ingredient_id: int
    quantity: float
    unit: str = "g"
    calories: float
    protein: float
    fat: float
    carbs: float


class RecipeUnstruction(BaseModel):
    step: int
    description: str
    time_minutes: Optional[int] = None


class Recipe(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    description: str
    category_id: int
    cook_time_minutes: int
    portions: int
    difficulty: str = "easy"
    ingredients: List[RecipeIngridient]
    instructions: List[RecipeUnstruction]
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    calories_per_portion: float
    protein_per_portion: float
    fat_per_portion: float
    carbs_per_portion: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
