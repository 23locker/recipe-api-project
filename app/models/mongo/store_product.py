from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class StoreProduct(BaseModel):
    id: Optional[str] = Field(alias="_id")
    ingredient_id: int
    name: str
    price: float
    source: str = "Пятерочка"
    url: str
    characteristics: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
