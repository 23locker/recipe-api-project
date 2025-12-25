from typing import Any, Dict, List, Optional

from tortoise.exceptions import DoesNotExist

from app.models.tortoise.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse


class CategoryService:
    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        category = await Category.create(**category_data)
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "created_at": category.created_at,
        }

    async def get_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        try:
            category = await Category.get(id=category_id)
            return {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "created_at": category.created_at,
            }
        except DoesNotExist:
            return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        categories = await Category.all()
        return [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "created_at": category.created_at,
            }
            for category in categories
        ]

    async def update_category(
        self, category_id: int, category_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            category = await Category.get(id=category_id)
            await category.update_from_dict(category_data)
            await category.save()
            return {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "created_at": category.created_at,
            }
        except DoesNotExist:
            return None

    async def delete_category(self, category_id: int) -> bool:
        try:
            category = await Category.get(id=category_id)
            await category.delete()
            return True
        except DoesNotExist:
            return False
