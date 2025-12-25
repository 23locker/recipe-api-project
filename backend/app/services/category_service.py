from fastapi import HTTPException, status

from app.models.tortoise.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    async def create_category(self, data: CategoryCreate) -> Category:
        exists = await Category.get_or_none(name=data.name)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists",
            )

        return await Category.create(**data.dict())

    async def get_category(self, category_id: int) -> Category | None:
        return await Category.get_or_none(id=category_id)

    async def get_all_categories(self) -> list[Category]:
        return await Category.all()

    async def update_category(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Category | None:
        category = await Category.get_or_none(id=category_id)
        if not category:
            return None

        if data.name and data.name != category.name:
            exists = await Category.get_or_none(name=data.name)
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category with this name already exists",
                )

        category.update_from_dict(data.dict(exclude_unset=True))
        await category.save()
        return category

    async def delete_category(self, category_id: int) -> bool:
        deleted_count = await Category.filter(id=category_id).delete()
        return deleted_count > 0
