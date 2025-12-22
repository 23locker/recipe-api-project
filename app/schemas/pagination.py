from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    data: List[T]
    next_cursor: Optional[str] = None
    has_more: bool
