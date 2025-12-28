from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_admin_user, get_current_user
from app.models.tortoise.user import User
from app.schemas.category import CategoryCreate, CategoryResponse, ListCategoryResponse
from app.services.category_service import CategoryService

router = APIRouter()
service = CategoryService()


@router.get(
    "",
    response_model=ListCategoryResponse,
)
async def get_all_categories():
    categories = await service.get_all_categories()
    return {"items": categories, "total": len(categories)}


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_data: CategoryCreate,
    _: User = Depends(get_admin_user),
):
    return await service.create_category(category_data)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def get_category(category_id: int):
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: int,
    category_data: CategoryCreate,  # or CategoryUpdate if you have one
    _: User = Depends(get_admin_user),
):
    updated = await service.update_category(category_id, category_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return updated


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: int,
    _: User = Depends(get_admin_user),
):
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
