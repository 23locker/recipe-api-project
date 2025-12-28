import asyncio

from app.db.mongodb import close_mongodb, get_mongodb, init_mongodb
from app.db.tortoise_config import close_tortoise, init_tortoise
from app.models.tortoise.category import Category
from app.models.tortoise.ingredient import Ingredient
from app.models.tortoise.substitute import Substitute
from app.models.tortoise.user import User
from app.services.recipe_service import RecipeService
from app.utils.security import hash_password


async def cleanup_data():
    """Удаление всех рецептов и ингредиентов"""
    print("🗑️  Удаление существующих данных...")

    db = await get_mongodb()
    result = await db.recipes.delete_many({})
    print(f"   ✅ Удалено {result.deleted_count} рецептов из MongoDB")

    sub_count = await Substitute.all().delete()
    print(f"   ✅ Удалено {sub_count} заменителей")

    ing_count = await Ingredient.all().delete()
    print(f"   ✅ Удалено {ing_count} ингредиентов")


async def seed_data():
    print("🚀 Начинаем заполнение базы данных данными")

    await init_tortoise()
    await init_mongodb()

    await cleanup_data()

    admin_user = await User.get_or_none(username="admin")
    if not admin_user:
        await User.create(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role="admin",
        )
        print("✅ Администратор создан")

    categories_data = [
        {"name": "Завтраки", "description": "Утренние блюда"},
        {"name": "Супы", "description": "Первые блюда"},
        {"name": "Горячие блюда", "description": "Основные блюда"},
        {"name": "Десерты", "description": "Сладкие блюда"},
        {"name": "Салаты", "description": "Холодные закуски"},
        {"name": "Мясо и птица", "description": "Мясные продукты"},
        {"name": "Овощи", "description": "Овощные продукты"},
        {"name": "Крупы", "description": "Крупы и макароны"},
        {"name": "Молочные продукты", "description": "Молочная продукция"},
    ]

    category_objs = {}
    for cat_data in categories_data:
        cat = await Category.get_or_create(name=cat_data["name"], defaults=cat_data)
        category_objs[cat_data["name"]] = cat[0]
    print(f"✅ {len(categories_data)} категорий создано")

    ingredients_data = [
        # Мясо и птица (10)
        {
            "name": "Куриное филе",
            "calories_per_100g": 110,
            "protein_per_100g": 23,
            "fat_per_100g": 2,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Говядина",
            "calories_per_100g": 250,
            "protein_per_100g": 26,
            "fat_per_100g": 15,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Свинина",
            "calories_per_100g": 242,
            "protein_per_100g": 16,
            "fat_per_100g": 21,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Индейка",
            "calories_per_100g": 104,
            "protein_per_100g": 22,
            "fat_per_100g": 1,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Утка",
            "calories_per_100g": 337,
            "protein_per_100g": 16,
            "fat_per_100g": 28,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Баранина",
            "calories_per_100g": 294,
            "protein_per_100g": 16,
            "fat_per_100g": 25,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Кролик",
            "calories_per_100g": 156,
            "protein_per_100g": 21,
            "fat_per_100g": 8,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Печень куриная",
            "calories_per_100g": 119,
            "protein_per_100g": 20,
            "fat_per_100g": 6,
            "carbs_per_100g": 1,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Фарш говяжий",
            "calories_per_100g": 254,
            "protein_per_100g": 17,
            "fat_per_100g": 20,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Сосиски",
            "calories_per_100g": 257,
            "protein_per_100g": 10,
            "fat_per_100g": 23,
            "carbs_per_100g": 1.5,
            "category_id": category_objs["Мясо и птица"].id,
        },
        # Овощи (15)
        {
            "name": "Картофель",
            "calories_per_100g": 77,
            "protein_per_100g": 2,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 16,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Морковь",
            "calories_per_100g": 41,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 9.6,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Лук репчатый",
            "calories_per_100g": 40,
            "protein_per_100g": 1.1,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 9,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Помидоры",
            "calories_per_100g": 18,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.2,
            "carbs_per_100g": 3.9,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Огурцы",
            "calories_per_100g": 15,
            "protein_per_100g": 0.8,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 2.8,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Капуста белокочанная",
            "calories_per_100g": 27,
            "protein_per_100g": 1.8,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 4.7,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Перец болгарский",
            "calories_per_100g": 27,
            "protein_per_100g": 1.3,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 5.3,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Баклажаны",
            "calories_per_100g": 24,
            "protein_per_100g": 1.2,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 4.5,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Кабачки",
            "calories_per_100g": 24,
            "protein_per_100g": 0.6,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 4.6,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Свекла",
            "calories_per_100g": 43,
            "protein_per_100g": 1.5,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 8.8,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Чеснок",
            "calories_per_100g": 149,
            "protein_per_100g": 6.5,
            "fat_per_100g": 0.5,
            "carbs_per_100g": 30,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Укроп",
            "calories_per_100g": 43,
            "protein_per_100g": 2.5,
            "fat_per_100g": 0.5,
            "carbs_per_100g": 6.3,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Петрушка",
            "calories_per_100g": 36,
            "protein_per_100g": 3,
            "fat_per_100g": 0.8,
            "carbs_per_100g": 7.6,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Салат листовой",
            "calories_per_100g": 12,
            "protein_per_100g": 1.2,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 1.3,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Редис",
            "calories_per_100g": 16,
            "protein_per_100g": 1.2,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 3.4,
            "category_id": category_objs["Овощи"].id,
        },
        # Крупы и макароны (8)
        {
            "name": "Рис",
            "calories_per_100g": 130,
            "protein_per_100g": 2.7,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 28,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Гречка",
            "calories_per_100g": 123,
            "protein_per_100g": 4.5,
            "fat_per_100g": 1.6,
            "carbs_per_100g": 25,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Макароны",
            "calories_per_100g": 150,
            "protein_per_100g": 5,
            "fat_per_100g": 1,
            "carbs_per_100g": 30,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Овсянка",
            "calories_per_100g": 68,
            "protein_per_100g": 2.4,
            "fat_per_100g": 1.4,
            "carbs_per_100g": 12,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Пшено",
            "calories_per_100g": 119,
            "protein_per_100g": 3.5,
            "fat_per_100g": 1,
            "carbs_per_100g": 23,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Манка",
            "calories_per_100g": 98,
            "protein_per_100g": 3,
            "fat_per_100g": 0.2,
            "carbs_per_100g": 21,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Перловка",
            "calories_per_100g": 109,
            "protein_per_100g": 3.1,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 22,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Булгур",
            "calories_per_100g": 83,
            "protein_per_100g": 3.1,
            "fat_per_100g": 0.2,
            "carbs_per_100g": 19,
            "category_id": category_objs["Крупы"].id,
        },
        # Молочные продукты (10)
        {
            "name": "Молоко",
            "calories_per_100g": 42,
            "protein_per_100g": 3.4,
            "fat_per_100g": 1.5,
            "carbs_per_100g": 5,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Сыр Гауда",
            "calories_per_100g": 350,
            "protein_per_100g": 25,
            "fat_per_100g": 27,
            "carbs_per_100g": 0,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Творог",
            "calories_per_100g": 101,
            "protein_per_100g": 16,
            "fat_per_100g": 2,
            "carbs_per_100g": 3.3,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Сметана",
            "calories_per_100g": 115,
            "protein_per_100g": 2.8,
            "fat_per_100g": 10,
            "carbs_per_100g": 3.2,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Кефир",
            "calories_per_100g": 40,
            "protein_per_100g": 2.8,
            "fat_per_100g": 1,
            "carbs_per_100g": 4,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Йогурт натуральный",
            "calories_per_100g": 58,
            "protein_per_100g": 3.5,
            "fat_per_100g": 1.5,
            "carbs_per_100g": 7.7,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Масло сливочное",
            "calories_per_100g": 717,
            "protein_per_100g": 0.8,
            "fat_per_100g": 81,
            "carbs_per_100g": 1.3,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Сливки",
            "calories_per_100g": 119,
            "protein_per_100g": 2.3,
            "fat_per_100g": 10,
            "carbs_per_100g": 4.8,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Сыр Моцарелла",
            "calories_per_100g": 280,
            "protein_per_100g": 28,
            "fat_per_100g": 17,
            "carbs_per_100g": 3,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Сыр Пармезан",
            "calories_per_100g": 392,
            "protein_per_100g": 36,
            "fat_per_100g": 26,
            "carbs_per_100g": 4,
            "category_id": category_objs["Молочные продукты"].id,
        },
        # Яйца (2)
        {
            "name": "Яйцо куриное",
            "calories_per_100g": 155,
            "protein_per_100g": 13,
            "fat_per_100g": 11,
            "carbs_per_100g": 1.1,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Яйцо перепелиное",
            "calories_per_100g": 168,
            "protein_per_100g": 11.9,
            "fat_per_100g": 13.1,
            "carbs_per_100g": 0.6,
            "category_id": category_objs["Молочные продукты"].id,
        },
        # Рыба и морепродукты (8)
        {
            "name": "Лосось",
            "calories_per_100g": 142,
            "protein_per_100g": 20,
            "fat_per_100g": 6,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Треска",
            "calories_per_100g": 82,
            "protein_per_100g": 17.7,
            "fat_per_100g": 0.7,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Скумбрия",
            "calories_per_100g": 191,
            "protein_per_100g": 18,
            "fat_per_100g": 13,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Креветки",
            "calories_per_100g": 99,
            "protein_per_100g": 24,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 0.2,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Кальмары",
            "calories_per_100g": 92,
            "protein_per_100g": 18,
            "fat_per_100g": 2.2,
            "carbs_per_100g": 2,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Мидии",
            "calories_per_100g": 77,
            "protein_per_100g": 11.5,
            "fat_per_100g": 2,
            "carbs_per_100g": 3.3,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Тунец консервированный",
            "calories_per_100g": 96,
            "protein_per_100g": 23,
            "fat_per_100g": 0.6,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        {
            "name": "Сельдь",
            "calories_per_100g": 161,
            "protein_per_100g": 17,
            "fat_per_100g": 10,
            "carbs_per_100g": 0,
            "category_id": category_objs["Мясо и птица"].id,
        },
        # Хлеб и выпечка (5)
        {
            "name": "Хлеб белый",
            "calories_per_100g": 266,
            "protein_per_100g": 7.6,
            "fat_per_100g": 3.3,
            "carbs_per_100g": 51,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Хлеб черный",
            "calories_per_100g": 214,
            "protein_per_100g": 6.6,
            "fat_per_100g": 1.2,
            "carbs_per_100g": 40,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Батон",
            "calories_per_100g": 260,
            "protein_per_100g": 7.5,
            "fat_per_100g": 2.9,
            "carbs_per_100g": 50,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Лаваш",
            "calories_per_100g": 277,
            "protein_per_100g": 9.1,
            "fat_per_100g": 1,
            "carbs_per_100g": 57,
            "category_id": category_objs["Крупы"].id,
        },
        {
            "name": "Слоеное тесто",
            "calories_per_100g": 337,
            "protein_per_100g": 5.6,
            "fat_per_100g": 17,
            "carbs_per_100g": 40,
            "category_id": category_objs["Крупы"].id,
        },
        # Масла и соусы (5)
        {
            "name": "Масло растительное",
            "calories_per_100g": 899,
            "protein_per_100g": 0,
            "fat_per_100g": 99.9,
            "carbs_per_100g": 0,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Масло оливковое",
            "calories_per_100g": 884,
            "protein_per_100g": 0,
            "fat_per_100g": 100,
            "carbs_per_100g": 0,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Майонез",
            "calories_per_100g": 629,
            "protein_per_100g": 3.1,
            "fat_per_100g": 67,
            "carbs_per_100g": 2.6,
            "category_id": category_objs["Молочные продукты"].id,
        },
        {
            "name": "Соевый соус",
            "calories_per_100g": 51,
            "protein_per_100g": 6,
            "fat_per_100g": 0,
            "carbs_per_100g": 5.6,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Томатная паста",
            "calories_per_100g": 102,
            "protein_per_100g": 4.8,
            "fat_per_100g": 0.5,
            "carbs_per_100g": 19,
            "category_id": category_objs["Овощи"].id,
        },
        # Фрукты и ягоды (7)
        {
            "name": "Яблоки",
            "calories_per_100g": 52,
            "protein_per_100g": 0.4,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 14,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Бананы",
            "calories_per_100g": 89,
            "protein_per_100g": 1.1,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 23,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Апельсины",
            "calories_per_100g": 47,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 12,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Лимон",
            "calories_per_100g": 29,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.1,
            "carbs_per_100g": 9,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Клубника",
            "calories_per_100g": 32,
            "protein_per_100g": 0.8,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 7.7,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Черника",
            "calories_per_100g": 57,
            "protein_per_100g": 0.7,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 14,
            "category_id": category_objs["Овощи"].id,
        },
        {
            "name": "Малина",
            "calories_per_100g": 52,
            "protein_per_100g": 1.2,
            "fat_per_100g": 0.7,
            "carbs_per_100g": 12,
            "category_id": category_objs["Овощи"].id,
        },
    ]

    ing_objs = {}
    for ing_data in ingredients_data:
        ing = await Ingredient.get_or_create(name=ing_data["name"], defaults=ing_data)
        ing_objs[ing_data["name"]] = ing[0]
    print(f"✅ {len(ingredients_data)} ингредиентов создано")

    recipe_service = RecipeService()
    recipes_list = [
        # Завтраки (6)
        {
            "name": "Омлет с сыром",
            "description": "Классический завтрак за 5 минут",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 10,
            "portions": 2,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Молоко"].id, "quantity": 50, "unit": "мл"},
                {
                    "ingredient_id": ing_objs["Сыр Гауда"].id,
                    "quantity": 30,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Взбейте яйца с молоком"},
                {"step": 2, "description": "Вылейте на разогретую сковороду"},
                {"step": 3, "description": "Посыпьте тертым сыром и сложите пополам"},
            ],
        },
        {
            "name": "Блины на молоке",
            "description": "Тонкие русские блины",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 30,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Молоко"].id, "quantity": 500, "unit": "мл"},
                {
                    "ingredient_id": ing_objs["Масло растительное"].id,
                    "quantity": 30,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Смешайте яйца с молоком"},
                {
                    "step": 2,
                    "description": "Добавьте муку и перемешайте до однородности",
                },
                {
                    "step": 3,
                    "description": "Жарьте на раскаленной сковороде с двух сторон",
                },
            ],
        },
        {
            "name": "Сырники с изюмом",
            "description": "Нежные творожные сырники",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 20,
            "portions": 3,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Творог"].id, "quantity": 300, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 50,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло растительное"].id,
                    "quantity": 20,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Смешайте творог с яйцом и мукой"},
                {"step": 2, "description": "Сформируйте сырники"},
                {"step": 3, "description": "Обжарьте до золотистой корочки"},
            ],
        },
        {
            "name": "Овсяная каша с ягодами",
            "description": "Полезный завтрак с ягодами",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 15,
            "portions": 2,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Овсянка"].id, "quantity": 100, "unit": "г"},
                {"ingredient_id": ing_objs["Молоко"].id, "quantity": 300, "unit": "мл"},
                {"ingredient_id": ing_objs["Клубника"].id, "quantity": 50, "unit": "г"},
                {"ingredient_id": ing_objs["Черника"].id, "quantity": 50, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Залейте овсянку молоком"},
                {"step": 2, "description": "Варите 10 минут"},
                {"step": 3, "description": "Добавьте свежие ягоды"},
            ],
        },
        {
            "name": "Яичница с помидорами",
            "description": "Быстрый и вкусный завтрак",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 10,
            "portions": 2,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Помидоры"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло растительное"].id,
                    "quantity": 15,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Нарежьте помидоры кубиками"},
                {"step": 2, "description": "Обжарьте помидоры на масле"},
                {"step": 3, "description": "Добавьте яйца и жарьте до готовности"},
            ],
        },
        {
            "name": "Творожная запеканка",
            "description": "Нежная запеканка из творога",
            "category_id": category_objs["Завтраки"].id,
            "cook_time_minutes": 40,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {"ingredient_id": ing_objs["Творог"].id, "quantity": 500, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Сметана"].id, "quantity": 50, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Смешайте все ингредиенты"},
                {"step": 2, "description": "Выложите в форму"},
                {"step": 3, "description": "Запекайте 30 минут при 180°C"},
            ],
        },
        # Супы (6)
        {
            "name": "Борщ",
            "description": "Традиционный украинский борщ",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 90,
            "portions": 6,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Говядина"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Свекла"].id, "quantity": 200, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Капуста белокочанная"].id,
                    "quantity": 200,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Сварите мясной бульон"},
                {"step": 2, "description": "Добавьте овощи"},
                {"step": 3, "description": "Варите до готовности"},
            ],
        },
        {
            "name": "Щи",
            "description": "Русские щи из свежей капусты",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 60,
            "portions": 6,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Говядина"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Капуста белокочанная"].id,
                    "quantity": 400,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Сварите бульон из говядины"},
                {"step": 2, "description": "Добавьте нашинкованную капусту"},
                {"step": 3, "description": "Добавьте картофель и варите до готовности"},
            ],
        },
        {
            "name": "Солянка мясная",
            "description": "Сытная солянка с мясом",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 70,
            "portions": 6,
            "difficulty": "Hard",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Говядина"].id,
                    "quantity": 200,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Свинина"].id, "quantity": 200, "unit": "г"},
                {"ingredient_id": ing_objs["Сосиски"].id, "quantity": 100, "unit": "г"},
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 150, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Сварите мясной бульон"},
                {"step": 2, "description": "Добавьте нарезанное мясо и сосиски"},
                {"step": 3, "description": "Добавьте соленые огурцы и томатную пасту"},
            ],
        },
        {
            "name": "Куриный суп с лапшой",
            "description": "Легкий куриный суп",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 40,
            "portions": 4,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Куриное филе"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Макароны"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 50,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Сварите куриный бульон"},
                {"step": 2, "description": "Добавьте овощи"},
                {"step": 3, "description": "Добавьте лапшу за 10 минут до готовности"},
            ],
        },
        {
            "name": "Грибной суп",
            "description": "Ароматный суп с грибами",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 50,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Сметана"].id, "quantity": 100, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Обжарьте грибы с луком"},
                {"step": 2, "description": "Добавьте картофель и воду"},
                {
                    "step": 3,
                    "description": "Варите до готовности, подавайте со сметаной",
                },
            ],
        },
        {
            "name": "Рассольник",
            "description": "Суп с солеными огурцами",
            "category_id": category_objs["Супы"].id,
            "cook_time_minutes": 60,
            "portions": 6,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Говядина"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 200, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Перловка"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 100, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Сварите бульон с перловкой"},
                {"step": 2, "description": "Добавьте картофель"},
                {
                    "step": 3,
                    "description": "Добавьте соленые огурцы за 10 минут до готовности",
                },
            ],
        },
        # Горячие блюда (10)
        {
            "name": "Курица с картофелем",
            "description": "Сытный ужин для всей семьи",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 45,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Куриное филе"].id,
                    "quantity": 500,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 800,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Нарежьте курицу и картофель кубиками"},
                {"step": 2, "description": "Обжарьте лук до золотистого цвета"},
                {"step": 3, "description": "Запекайте все вместе в духовке при 180°C"},
            ],
        },
        {
            "name": "Котлеты по-киевски",
            "description": "Классические котлеты с маслом",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 40,
            "portions": 4,
            "difficulty": "Hard",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Куриное филе"].id,
                    "quantity": 600,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло сливочное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отбейте филе и заверните в него масло"},
                {"step": 2, "description": "Обваляйте в яйце и сухарях"},
                {"step": 3, "description": "Жарьте во фритюре до золотистой корочки"},
            ],
        },
        {
            "name": "Голубцы",
            "description": "Традиционные голубцы с мясом",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 90,
            "portions": 6,
            "difficulty": "Hard",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Фарш говяжий"].id,
                    "quantity": 500,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Капуста белокочанная"].id,
                    "quantity": 600,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Рис"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Томатная паста"].id,
                    "quantity": 50,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отварите капустные листья"},
                {"step": 2, "description": "Заверните фарш с рисом в листья"},
                {"step": 3, "description": "Тушите в томатном соусе 60 минут"},
            ],
        },
        {
            "name": "Плов",
            "description": "Узбекский плов с бараниной",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 90,
            "portions": 6,
            "difficulty": "Hard",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Баранина"].id,
                    "quantity": 500,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Рис"].id, "quantity": 500, "unit": "г"},
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 300, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 200,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Обжарьте мясо с луком и морковью"},
                {"step": 2, "description": "Добавьте рис и воду"},
                {"step": 3, "description": "Томите под крышкой до готовности"},
            ],
        },
        {
            "name": "Жаркое",
            "description": "Мясо с овощами в горшочке",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 120,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {"ingredient_id": ing_objs["Свинина"].id, "quantity": 400, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 500,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 150, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Нарежьте мясо и овощи"},
                {"step": 2, "description": "Уложите слоями в горшочки"},
                {"step": 3, "description": "Запекайте 90 минут при 180°C"},
            ],
        },
        {
            "name": "Макароны по-флотски",
            "description": "Макароны с фаршем",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 30,
            "portions": 4,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Макароны"].id,
                    "quantity": 400,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Фарш говяжий"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отварите макароны"},
                {"step": 2, "description": "Обжарьте фарш с луком"},
                {"step": 3, "description": "Смешайте макароны с фаршем"},
            ],
        },
        {
            "name": "Рыба запеченная",
            "description": "Лосось в духовке",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 35,
            "portions": 3,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Лосось"].id, "quantity": 500, "unit": "г"},
                {"ingredient_id": ing_objs["Лимон"].id, "quantity": 50, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Масло оливковое"].id,
                    "quantity": 20,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Полейте рыбу лимонным соком"},
                {"step": 2, "description": "Смажьте оливковым маслом"},
                {"step": 3, "description": "Запекайте 25 минут при 200°C"},
            ],
        },
        {
            "name": "Тефтели в томатном соусе",
            "description": "Сочные тефтели с рисом",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 50,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Фарш говяжий"].id,
                    "quantity": 500,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Рис"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Томатная паста"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Смешайте фарш с отварным рисом"},
                {"step": 2, "description": "Сформируйте тефтели"},
                {"step": 3, "description": "Тушите в томатном соусе 30 минут"},
            ],
        },
        {
            "name": "Картофельное пюре с котлетами",
            "description": "Классическое сочетание",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 40,
            "portions": 4,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 800,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Фарш говяжий"].id,
                    "quantity": 400,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Молоко"].id, "quantity": 100, "unit": "мл"},
                {
                    "ingredient_id": ing_objs["Масло сливочное"].id,
                    "quantity": 50,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отварите картофель и сделайте пюре"},
                {"step": 2, "description": "Сформируйте котлеты из фарша"},
                {"step": 3, "description": "Обжарьте котлеты до готовности"},
            ],
        },
        {
            "name": "Гречка с грибами",
            "description": "Постное блюдо с грибами",
            "category_id": category_objs["Горячие блюда"].id,
            "cook_time_minutes": 35,
            "portions": 3,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Гречка"].id, "quantity": 300, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Лук репчатый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло растительное"].id,
                    "quantity": 30,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отварите гречку"},
                {"step": 2, "description": "Обжарьте грибы с луком"},
                {"step": 3, "description": "Смешайте гречку с грибами"},
            ],
        },
        # Салаты (5)
        {
            "name": "Оливье",
            "description": "Классический русский салат",
            "category_id": category_objs["Салаты"].id,
            "cook_time_minutes": 30,
            "portions": 6,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 300,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 150, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 100, "unit": "г"},
                {"ingredient_id": ing_objs["Майонез"].id, "quantity": 100, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Отварите овощи и яйца"},
                {"step": 2, "description": "Нарежьте все кубиками"},
                {"step": 3, "description": "Заправьте майонезом"},
            ],
        },
        {
            "name": "Винегрет",
            "description": "Овощной салат со свеклой",
            "category_id": category_objs["Салаты"].id,
            "cook_time_minutes": 25,
            "portions": 4,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Свекла"].id, "quantity": 200, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Картофель"].id,
                    "quantity": 200,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Морковь"].id, "quantity": 150, "unit": "г"},
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 100, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Масло растительное"].id,
                    "quantity": 50,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Отварите овощи"},
                {"step": 2, "description": "Нарежьте кубиками"},
                {"step": 3, "description": "Заправьте растительным маслом"},
            ],
        },
        {
            "name": "Цезарь",
            "description": "Салат Цезарь с курицей",
            "category_id": category_objs["Салаты"].id,
            "cook_time_minutes": 20,
            "portions": 3,
            "difficulty": "Medium",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Куриное филе"].id,
                    "quantity": 200,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Салат листовой"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Сыр Пармезан"].id,
                    "quantity": 50,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Хлеб белый"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Обжарьте курицу"},
                {"step": 2, "description": "Приготовьте сухарики из хлеба"},
                {"step": 3, "description": "Смешайте с салатом и заправкой"},
            ],
        },
        {
            "name": "Греческий салат",
            "description": "Свежий средиземноморский салат",
            "category_id": category_objs["Салаты"].id,
            "cook_time_minutes": 15,
            "portions": 3,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Помидоры"].id,
                    "quantity": 200,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 150, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Перец болгарский"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Сыр Моцарелла"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло оливковое"].id,
                    "quantity": 30,
                    "unit": "мл",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Нарежьте овощи крупными кусками"},
                {"step": 2, "description": "Добавьте кубики сыра"},
                {"step": 3, "description": "Заправьте оливковым маслом"},
            ],
        },
        {
            "name": "Салат с крабовыми палочками",
            "description": "Легкий салат с кукурузой",
            "category_id": category_objs["Салаты"].id,
            "cook_time_minutes": 15,
            "portions": 4,
            "difficulty": "Easy",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Огурцы"].id, "quantity": 100, "unit": "г"},
                {"ingredient_id": ing_objs["Майонез"].id, "quantity": 80, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Нарежьте крабовые палочки"},
                {"step": 2, "description": "Добавьте яйца и огурцы"},
                {"step": 3, "description": "Заправьте майонезом"},
            ],
        },
        # Десерты (3)
        {
            "name": "Шарлотка",
            "description": "Яблочный пирог",
            "category_id": category_objs["Десерты"].id,
            "cook_time_minutes": 50,
            "portions": 6,
            "difficulty": "Easy",
            "ingredients": [
                {"ingredient_id": ing_objs["Яблоки"].id, "quantity": 400, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {
                    "ingredient_id": ing_objs["Масло сливочное"].id,
                    "quantity": 50,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Взбейте яйца с сахаром"},
                {"step": 2, "description": "Добавьте муку и нарезанные яблоки"},
                {"step": 3, "description": "Выпекайте 40 минут при 180°C"},
            ],
        },
        {
            "name": "Медовик",
            "description": "Классический торт с медом",
            "category_id": category_objs["Десерты"].id,
            "cook_time_minutes": 120,
            "portions": 8,
            "difficulty": "Hard",
            "ingredients": [
                {
                    "ingredient_id": ing_objs["Яйцо куриное"].id,
                    "quantity": 150,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Сметана"].id, "quantity": 400, "unit": "г"},
                {
                    "ingredient_id": ing_objs["Масло сливочное"].id,
                    "quantity": 100,
                    "unit": "г",
                },
            ],
            "instructions": [
                {"step": 1, "description": "Приготовьте медовые коржи"},
                {"step": 2, "description": "Сделайте крем из сметаны"},
                {"step": 3, "description": "Соберите торт и дайте пропитаться"},
            ],
        },
        {
            "name": "Панакота с ягодами",
            "description": "Итальянский десерт",
            "category_id": category_objs["Десерты"].id,
            "cook_time_minutes": 30,
            "portions": 4,
            "difficulty": "Medium",
            "ingredients": [
                {"ingredient_id": ing_objs["Сливки"].id, "quantity": 400, "unit": "мл"},
                {
                    "ingredient_id": ing_objs["Клубника"].id,
                    "quantity": 100,
                    "unit": "г",
                },
                {"ingredient_id": ing_objs["Малина"].id, "quantity": 100, "unit": "г"},
            ],
            "instructions": [
                {"step": 1, "description": "Нагрейте сливки с сахаром"},
                {"step": 2, "description": "Добавьте желатин"},
                {
                    "step": 3,
                    "description": "Разлейте по формам и охладите, подавайте с ягодами",
                },
            ],
        },
    ]

    for r_data in recipes_list:
        await recipe_service.create_recipe(r_data)
    print(f"✅ {len(recipes_list)} рецептов создано")

    await close_tortoise()
    await close_mongodb()
    print("✨ Заполнение базы данных завершено!")
    print(
        f"📊 Итого: {len(ingredients_data)} ингредиентов и {len(recipes_list)} рецептов"
    )


if __name__ == "__main__":
    asyncio.run(seed_data())
