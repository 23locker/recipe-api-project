from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.models.tortoise.category import Category
from app.models.tortoise.ingredient import Ingredient
from app.models.tortoise.substitute import Substitute


class IngredientService:
    async def get_ingredient(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """
        Получить ингредиент по ID
        """
        try:
            ingredient = await Ingredient.get(id=ingredient_id)

            return {
                "id": ingredient.id,
                "name": ingredient.name,
                "calories_per_100g": ingredient.calories_per_100g,
                "protein_per_100g": ingredient.protein_per_100g,
                "fat_per_100g": ingredient.fat_per_100g,
                "carbs_per_100g": ingredient.carbs_per_100g,
                "category_id": ingredient.category,
                "created_at": ingredient.created_at,
            }
        except DoesNotExist:
            return None

    async def get_all_ingredients(
        self, size: int = 50, cursor: Optional[str] = None
    ) -> dict:
        """
        Получить все ингредиенты с пагинацией
        """
        query = Ingredient.all()

        if cursor:
            try:
                cursor_id = int(cursor)
                query = query.filter(id__gt=cursor_id)
            except Exception:
                pass

        ingredients = await query.order_by("id").limit(size + 1)

        has_more = len(ingredients) > size
        next_cursor = None
        if ingredients and has_more:
            next_cursor = str(ingredients[-1].id)
            ingredients = ingredients[:-1]

        data = []
        for ing in ingredients:
            data.append(
                {
                    "id": ing.id,
                    "name": ing.name,
                    "calories_per_100g": ing.calories_per_100g,
                    "protein_per_100g": ing.protein_per_100g,
                    "fat_per_100g": ing.fat_per_100g,
                    "carbs_per_100g": ing.carbs_per_100g,
                    "category_id": ing.category,
                    "created_at": ing.created_at,
                }
            )

        return {
            "data": data,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }

    async def create_ingredient(self, ingredient_data: dict) -> Ingredient:
        """
        Создание ингредиента
        """
        category_id = ingredient_data.get("category_id")
        name = ingredient_data.get("name")

        try:
            await Category.get(id=category_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {category_id} does not exist",
            )

        existing = await Ingredient.get_or_none(name=name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ingredient with name '{name}' already exists",
            )

        ingredient = await Ingredient.create(**ingredient_data)
        return ingredient

    async def get_substitutes(self, ingredient_id: int) -> List[Dict[str, Any]]:
        """
        Получить ВСЕ замены ингредиента
        """
        substitutes = await Substitute.filter(original_ingredient_id=ingredient_id)

        result = []
        for substitute in substitutes:
            sub_ingredient = await Ingredient.get(id=substitute.substitute_ingredient)
            result.append(
                {
                    "id": substitute.id,
                    "original_ingredient_id": substitute.original_ingredient,
                    "substitute_ingredient_id": substitute.substitute_ingredient,
                    "substitute_name": sub_ingredient.name,
                    "coefficient": substitute.coefficient,
                    "created_at": substitute.created_at,
                }
            )

        return result

    async def get_substitute(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """
        Получаем первую замену для ингредиента
        """
        try:
            substitute = await Substitute.filter(
                original_ingredient_id=ingredient_id
            ).first()
            if substitute:
                return {
                    "original_ingredient_id": substitute.original_ingredient,
                    "substitute_ingredient_id": substitute.substitute_ingredient,
                    "coefficient": substitute.coefficient,
                }
            return None
        except Exception:
            return None

    async def create_substitute(self, substitute_data: Dict[str, Any]) -> Substitute:
        """
        Создание замены
        """
        orig_id = substitute_data["original_ingredient_id"]
        sub_id = substitute_data["substitute_ingredient_id"]

        if orig_id == sub_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient cannot be a substitute for itself",
            )

        # Проверка существования обоих ингредиентов
        orig_exists = await Ingredient.exists(id=orig_id)
        sub_exists = await Ingredient.exists(id=sub_id)

        if not orig_exists or not sub_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both ingredients do not exist",
            )

        substitute = await Substitute.create(**substitute_data)
        return substitute
