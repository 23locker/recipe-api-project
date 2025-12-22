from datetime import datetime

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    descriptiton: str = None


class CatregoryResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
