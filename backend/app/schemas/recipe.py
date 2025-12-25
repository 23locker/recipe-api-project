from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity: float
    unit: str = "g"


class RecipeIngredientResponse(BaseModel):
    ingredient_id: int
    quantity: float
    unit: str
    calories: float
    protein: float
    fat: float
    carbs: float


class RecipeInstructionCreate(BaseModel):
    step: int
    description: str
    time_minutes: Optional[int] = None


class RecipeInstructionResponse(BaseModel):
    step: int
    description: str
    time_minutes: Optional[int] = None


class RecipeCreate(BaseModel):
    name: str
    description: str
    category_id: int
    cook_time_minutes: int
    portions: int
    difficulty: str = "easy"
    ingredients: List[RecipeIngredientCreate]
    instructions: List[RecipeInstructionCreate]


class RecipeResponse(BaseModel):
    id: str
    name: str
    description: str
    category_id: int
    cook_time_minutes: int
    portions: int
    difficulty: str
    ingredients: List[RecipeIngredientResponse]
    instructions: List[RecipeInstructionResponse]
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    calories_per_portion: float
    protein_per_portion: float
    fat_per_portion: float
    carbs_per_portion: float
    created_at: datetime
    updated_at: datetime
