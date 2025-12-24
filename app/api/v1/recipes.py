from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_admin_user, get_current_user
from app.models.tortoise.user import User
from app.schemas.recipe import RecipeCreate, RecipeResponse
from app.services.recipe_service import RecipeService

router = APIRouter(tags=["recipes"])
recipe_service = RecipeService()


@router.get("", response_model=dict)
async def get_recipes(
    cursor: Optional[str] = Query(None),
    size: int = Query(30, le=50),
    category_id: Optional[int] = None,
    min_calories: Optional[float] = None,
    max_calories: Optional[float] = None,
    max_time: Optional[int] = None,
    exclude_ingredients: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
):
    """
    Получить список рецептов с пагинацией

    query параметры:
    - cursor: курсор для следующей страницы (опционально)
    - size: количество рецептов на странице (по умолчанию 30, максимум 50)
    - category_id: фильтр по категории (опционально)
    - min_calories: минимальные калории (опционально)
    - max_calories: максимальные калории (опционально)
    - max_time: максимальное время приготовления в минутах (опционально)
    - exclude_ingredients: ID ингредиентов для исключения через запятую (опционально)
    """
    exclude_list = None
    if exclude_ingredients:
        try:
            exclude_list = [int(x) for x in exclude_ingredients.split(",")]
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exclude_ingredients format",
            )

    return await recipe_service.get_recipes(
        cursor=cursor,
        size=size,
        category_id=category_id,
        min_calories=min_calories,
        max_calories=max_calories,
        max_time=max_time,
        exclude_ingredients=exclude_list,
    )


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: str, current_user: User = Depends(get_current_user)):
    """Получить рецепт по ID"""
    recipe = await recipe_service.get_recipe(recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    return recipe


@router.post("", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate, current_user: User = Depends(get_admin_user)
):
    """Создать новый рецепт (только администратор)"""
    if len(recipe.ingredients) < 2 or len(recipe.ingredients) > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe must have between 2 and 30 ingredients",
        )

    recipe_data = recipe.dict()
    created_recipe = await recipe_service.create_recipe(recipe_data)

    return created_recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: str, recipe: RecipeCreate, current_user: User = Depends(get_admin_user)
):
    """Обновить рецепт (только админ)"""
    existing_recipe = await recipe_service.get_recipe(recipe_id)

    if not existing_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    recipe_data = recipe.dict()
    updated_recipe = await recipe_service.update_recipe(recipe_id, recipe_data)

    return updated_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: str, current_user: User = Depends(get_admin_user)):
    """Удалить рецепт (только админ)"""
    recipe = await recipe_service.get_recipe(recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    await recipe_service.delete_recipe(recipe_id)


@router.post("/{recipe_id}/with-substitutes", response_model=RecipeResponse)
async def get_recipe_with_substitutes(
    recipe_id: str,
    unavailable_ingredients: List[dict],
    current_user: User = Depends(get_current_user),
):
    """
    Получить рецепт с заменами ингредиентов

    body: {
        "unavailable_ingredients": [
            {"ingredient_id": 1},
            {"ingredient_id": 5}
        ]
    }
    """
    recipe = await recipe_service.get_recipe_with_subtitutes(
        recipe_id=recipe_id, unavailable_ingredients=unavailable_ingredients
    )

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found or cannot be made with substitutes",
        )

    return recipe
