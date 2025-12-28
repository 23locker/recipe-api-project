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
    size: int = Query(50, le=200),
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


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientCreate,
    current_user: User = Depends(get_admin_user),
):
    """
    Обновить ингредиент (только админ)
    """
    updated = await ingredient_service.update_ingredient(
        ingredient_id, ingredient.model_dump()
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return updated


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_admin_user),
):
    """
    Удалить ингредиент (только админ)
    """
    success = await ingredient_service.delete_ingredient(ingredient_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return None


@router.get("/{ingredient_id}/substitutes", response_model=List[SubstituteResponse])
async def get_substitutes(
    ingredient_id: int, current_user: User = Depends(get_current_user)
):
    """Получить все замены для ингредиента"""
    return await ingredient_service.get_substitutes(ingredient_id)


@router.get("/substitutes/all", response_model=List[SubstituteResponse])
async def get_all_substitutes(current_user: User = Depends(get_current_user)):
    """Получить все замены ингредиентов"""
    return await ingredient_service.get_all_substitutes()


@router.post("/substitutes", response_model=SubstituteResponse)
async def create_substitute(
    substitute: SubstituteCreate, current_user: User = Depends(get_admin_user)
):
    """Создать замену для ингредиента (только администратор)"""
    created = await ingredient_service.create_substitute(substitute.dict())
    return created


@router.delete("/substitutes/{substitute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_substitute(
    substitute_id: int, current_user: User = Depends(get_admin_user)
):
    """Удалить замену ингредиента (только администратор)"""
    success = await ingredient_service.delete_substitute(substitute_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Substitute not found",
        )
    
    return None
