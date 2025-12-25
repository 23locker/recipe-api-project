from datetime import datetime

from pydantic import BaseModel, Field


class SubstituteCreate(BaseModel):
    original_ingredient_id: int
    substitute_ingredient_id: int
    coefficient: float = Field(gt=0, le=3)


class SubstituteResponse(BaseModel):
    id: int
    original_ingredient_id: int
    substitute_ingredient_id: int
    coefficient: float
    created_at: datetime

    class Config:
        from_attributes = True
