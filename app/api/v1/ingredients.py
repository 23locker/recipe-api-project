from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_admin_user, get_current_user
from app.models.tortoise.user import User
from app.schemas.ingredient import IngredientCreate, IngredientResponse
from app.schemas.substitute import SubstituteCreate, SubstituteResponse
from app.services.ingredient_service import IngredientService

router = APIRouter(tags=["ingredients"])
ingredient_service = IngredientService()


@router.get("", response_model=dict)
async def get_ingredients(
    cursor: Optional[str] = Query(None),
    size: int = Query(50, le=50),
    current_user: User = Depends(get_current_user),
):
    """
    Получить список всех ингредиентов с пагинацией
    """
    return await ingredient_service.get_all_ingredients(size=size, cursor=cursor)


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Получить ингредиент по ID
    """
    ingredient = await ingredient_service.get_ingredient(ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return ingredient


@router.post("", response_model=IngredientResponse)
async def create_ingredient(
    ingredient: IngredientCreate,
    current_user: User = Depends(get_admin_user),
):
    """
    Создать новый ингредиент (только админ)
    """
    created = await ingredient_service.create_ingredient(ingredient.model_dump())
    return created


@router.get("/{ingredient_id}/substitutes", response_model=List[SubstituteResponse])
async def get_substitutes(
    ingredient_id: int, current_user: User = Depends(get_current_user)
):
    """Получить все замены для ингредиента"""
    return await ingredient_service.get_substitutes(ingredient_id)


@router.post("/substitutes", response_model=SubstituteResponse)
async def create_substitute(
    substitute: SubstituteCreate, current_user: User = Depends(get_admin_user)
):
    """Создать замену для ингредиента (только администратор)"""
    created = await ingredient_service.create_substitute(substitute.dict())
    return created
