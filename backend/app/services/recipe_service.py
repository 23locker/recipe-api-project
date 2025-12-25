from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.db.mongodb import get_mongodb
from app.models.mongo.recipe import Recipe, RecipeIngredient, RecipeInstruction
from app.services.ingredient_service import IngredientService


class RecipeService:
    def __init__(self) -> None:
        self.db: AsyncIOMotorDatabase = None
        self.collection: AsyncIOMotorCollection = None
        self.ingredient_service = IngredientService()

    async def _get_collection(self):
        if self.collection is None:
            self.db = await get_mongodb()
            self.collection = self.db.recipes
        return self.collection

    async def get_recipes(
        self,
        cursor: Optional[str] = None,
        size: int = 30,
        category_id: Optional[str] = None,
        min_calories: Optional[float] = None,
        max_calories: Optional[float] = None,
        max_time: Optional[int] = None,
        exclude_ingredients: Optional[List[int]] = None,
    ) -> dict:
        """
        Получить писок рецептов с пагинацией (cursor-based)
        """
        collection = await self._get_collection()

        filters = {}

        if category_id:
            filters["category_id"] = category_id

        if min_calories is not None or max_calories is not None:
            filters["total_calories"] = {}
            if min_calories is not None:
                filters["total_calories"]["$gte"] = min_calories
            if max_calories is not None:
                filters["total_calories"]["$lte"] = max_calories

        if max_time:
            filters["cook_time_minutes"] = {"$lte": max_time}

        if exclude_ingredients:
            filters["ingredients.ingredients_id"] = {"$nin": exclude_ingredients}

        if cursor:
            try:
                filters["_id"] = {"$gt": ObjectId(cursor)}
            except Exception:
                pass

        recipes = (
            await collection.find(filters)
            .sort("_id", 1)
            .limit(size + 1)
            .to_list(size + 1)
        )

        has_more = len(recipes) > size
        if has_more:
            recipes = recipes[:size]

        next_cursor = None
        if recipes and has_more:
            next_cursor = str(recipes[-1]["_id"])

        # Convert _id to id for serialization
        for recipe in recipes:
            recipe["id"] = str(recipe.pop("_id"))

        return {
            "data": recipes,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }

    async def get_recipe(self, recipe_id: str) -> Optional[dict]:
        """
        Берем рецепт по его ID
        """
        collection = await self._get_collection()

        try:
            recipe = await collection.find_one({"_id": ObjectId(recipe_id)})
            if recipe:
                recipe["id"] = str(recipe.pop("_id"))
            return recipe
        except Exception:
            return None

    async def create_recipe(self, recipe_data: Dict[str, Any]) -> dict:
        """
        Создание нового рецепта
        """
        collection = await self._get_collection()

        recipe_dict = recipe_data.copy()

        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for ingredient in recipe_dict["ingredients"]:
            ing_data = await self.ingredient_service.get_ingredient(
                ingredient["ingredient_id"]
            )

            if not ing_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ingredient with ID {ingredient['ingredient_id']} not found",
                )

            quantity = ingredient["quantity"]
            calories = (ing_data["calories_per_100g"] / 100) * quantity
            protein = (ing_data["protein_per_100g"] / 100) * quantity
            fat = (ing_data["fat_per_100g"] / 100) * quantity
            carbs = (ing_data["carbs_per_100g"] / 100) * quantity

            ingredient["calories"] = calories
            ingredient["protein"] = protein
            ingredient["fat"] = fat
            ingredient["carbs"] = carbs

            total_calories += calories
            total_protein += protein
            total_fat += fat
            total_carbs += carbs

        portions = recipe_dict["portions"]

        recipe_dict["total_calories"] = round(total_calories, 2)
        recipe_dict["total_protein"] = round(total_protein, 2)
        recipe_dict["total_fat"] = round(total_fat, 2)
        recipe_dict["total_carbs"] = round(total_carbs, 2)

        recipe_dict["calories_per_portion"] = round(total_calories / portions, 2)
        recipe_dict["protein_per_portion"] = round(total_protein / portions, 2)
        recipe_dict["fat_per_portion"] = round(total_fat / portions, 2)
        recipe_dict["carbs_per_portion"] = round(total_carbs / portions, 2)

        recipe_dict["created_at"] = datetime.utcnow()
        recipe_dict["updated_at"] = datetime.utcnow()

        result = await collection.insert_one(recipe_dict)

        return await self.get_recipe(str(result.inserted_id))

    async def get_recipe_with_substitutes(
        self,
        recipe_id: str,
        unavailable_ingredients: List[Dict[str, int]],
    ) -> Optional[dict]:
        """
        Получить рецепт с заменами ингредиентов
        """
        recipe = await self.get_recipe(recipe_id)
        if not recipe:
            return None

        modified_recipe = recipe.copy()
        modified_recipe["ingredients"] = recipe["ingredients"].copy()

        unavailable_ids = [ing["ingredient_id"] for ing in unavailable_ingredients]

        new_ingredients = []
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for ingredient in modified_recipe["ingredients"]:
            if ingredient["ingredient_id"] in unavailable_ids:
                substitute = await self.ingredient_service.get_substitute(
                    ingredient["ingredient_id"]
                )

                if substitute:
                    new_ingredient = ingredient.copy()
                    new_ingredient["ingredient_id"] = substitute[
                        "substitute_ingredient_id"
                    ]
                    new_ingredient["quantity"] = (
                        ingredient["quantity"] * substitute["coefficient"]
                    )

                    new_ing_data = await self.ingredient_service.get_ingredient(
                        substitute["substitute_ingredient_id"]
                    )

                    if not new_ing_data:
                        # Если замена почему-то не найдена в базе, пропускаем или падаем? 
                        # Лучше пропустить этот вариант замены или вернуть ошибку.
                        continue

                    quantity = new_ingredient["quantity"]
                    new_ingredient["calories"] = round(
                        (new_ing_data["calories_per_100g"] / 100) * quantity, 2
                    )
                    new_ingredient["protein"] = round(
                        (new_ing_data["protein_per_100g"] / 100) * quantity, 2
                    )
                    new_ingredient["fat"] = round(
                        (new_ing_data["fat_per_100g"] / 100) * quantity, 2
                    )
                    new_ingredient["carbs"] = round(
                        (new_ing_data["carbs_per_100g"] / 100) * quantity, 2
                    )

                    new_ingredients.append(new_ingredient)

                    total_calories += new_ingredient["calories"]
                    total_protein += new_ingredient["protein"]
                    total_fat += new_ingredient["fat"]
                    total_carbs += new_ingredient["carbs"]
            else:
                new_ingredients.append(ingredient)
                total_calories += ingredient["calories"]
                total_protein += ingredient["protein"]
                total_fat += ingredient["fat"]
                total_carbs += ingredient["carbs"]

        if len(new_ingredients) < 2:
            return None

        portions = modified_recipe["portions"]
        modified_recipe["ingredients"] = new_ingredients
        modified_recipe["total_calories"] = round(total_calories, 2)
        modified_recipe["total_protein"] = round(total_protein, 2)
        modified_recipe["total_fat"] = round(total_fat, 2)
        modified_recipe["total_carbs"] = round(total_carbs, 2)

        modified_recipe["calories_per_portion"] = round(total_calories / portions, 2)
        modified_recipe["protein_per_portion"] = round(total_protein / portions, 2)
        modified_recipe["fat_per_portion"] = round(total_fat / portions, 2)
        modified_recipe["carbs_per_portion"] = round(total_carbs / portions, 2)

        return modified_recipe

    async def update_recipe(
        self, recipe_id: str, recipe_data: Dict[str, Any]
    ) -> Optional[dict]:
        """
        Обновление рецепта
        """
        collection = await self._get_collection()

        try:
            recipe_data["updated_at"] = datetime.utcnow()

            await collection.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": recipe_data},
            )

            return await self.get_recipe(recipe_id)

        except Exception:
            return None

    async def delete_recipe(self, recipe_id: str) -> bool:
        """
        Удаление рецепта
        """
        collection = await self._get_collection()

        try:
            result = await collection.delete_one({"_id": ObjectId(recipe_id)})
            return result.deleted_count > 0
        except Exception:
            return False
