from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class StoreProductCreate(BaseModel):
    ingredient_id: int
    name: str
    price: float
    source: str
    url: str
    characteristics: Optional[Dict[str, Any]] = None


class StoreProductResponse(BaseModel):
    id: str
    ingredient: str
    name: str
    price: float
    source: str
    url: str
    characteristics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
