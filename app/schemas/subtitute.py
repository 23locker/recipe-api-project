from datetime import datetime

from pydantic import BaseModel, Field


class SubtituteCreate(BaseModel):
    original_ingridient_id: int
    subtitute_ingridient_id: int
    coefficient: float = Field(gt=0, le=3)


class SubtituteResponse(BaseModel):
    id: int
    original_ingridient_id: int
    subtitute_ingridient_id: int
    coefficient: int
    created_at: datetime

    class Config:
        from_attributes = True
