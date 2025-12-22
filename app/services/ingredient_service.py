from typing import Any, Dict, List, Optional

from tortoise.exceptions import DoesNotExist

from app.models.tortoise.ingredient import Ingredient
from app.models.tortoise.substitute import Subtitute


class IngredientService:
    async def get_ingredient(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """
        Получить ингридиент по ID
        """
        try:
            ingredient = await Ingredient.get(id=ingredient_id)

            return {
                "id": ingredient.id,
                "name": ingredient.name,
                "calories_per_100g": ingredient.calories_per_100g,
                "proteion_per_100g": ingredient.protein_per_100g,
                "fat_per_100g": ingredient.fat_per_100g,
                "carbs_per_100g": ingredient.carbs_per_100g,
                "category_id": ingredient.category_id,
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
            except:
                pass

        ingredients = await query.order_by("id").limit(size + 1)

        has_more = len(ingredients) > size
        if ingredients and has_more:
            next_cursor = str(ingredients[-1].id)

        return {
            "data": ingredients,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }

    async def create_ingredient(self, ingredient_data: Dict[str, Any]) -> Ingredient:
        """
        Создание ингридиента
        """
        ingredient = await Ingredient.create(**ingredient_data)
        return ingredient

    async def get_subtitutes(self, ingredient_id: int) -> List[Dict[str, Any]]:
        """
        Получить ВСЕ замены ингредиента
        """
        substitutes = await Subtitute.filter(original_ingredient_id=ingredient_id)

        result = []
        for substitute in substitutes:
            sub_ingredient = await Ingredient.get(id=substitute.subtitutes_ingridient)
            result.append(
                {
                    "id": substitute.id,
                    "original_ingredient_id": substitute.original_ingredient_id,
                    "substitute_ingredient_id": substitute.substitute_ingredient_id,
                    "substitute_name": sub_ingredient.name,
                    "coefficient": substitute.coefficient,
                }
            )

        return result

    async def get_substitute(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """
        Получаем первую замену для ингредиента
        """
        try:
            subtitute = await Subtitute.filter(original_ingredient_id=ingredient_id)
            if subtitute:
                return {
                    "original_ingredient_id": subtitute.original_ingredient_id,
                    "subtitute_ingredient_id": subtitute.subtitute_ingredient_id,
                    "coefficient": subtitute.coefficient,
                }
            return None
        except:
            return None

    async def create_subtitute(self, subtitute_data: Dict[str, Any]) -> Subtitute:
        """
        Создание замены
        """
        subtitute = await Subtitute.create(**subtitute_data)
        return subtitute
