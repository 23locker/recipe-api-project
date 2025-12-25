import pytest


@pytest.fixture
async def setup_recipe_data(admin_client):
    cat_res = await admin_client.post("/api/v1/category", json={"name": "Dinner"})
    category_id = cat_res.json()["id"]

    ing1_res = await admin_client.post(
        "/api/v1/ingredients",
        json={
            "name": "Pasta",
            "calories_per_100g": 350,
            "protein_per_100g": 12,
            "fat_per_100g": 1.5,
            "carbs_per_100g": 70,
            "category_id": category_id,
        },
    )
    ing1_id = ing1_res.json()["id"]

    ing2_res = await admin_client.post(
        "/api/v1/ingredients",
        json={
            "name": "Tomato Sauce",
            "calories_per_100g": 50,
            "protein_per_100g": 1.5,
            "fat_per_100g": 0.5,
            "carbs_per_100g": 10,
            "category_id": category_id,
        },
    )
    ing2_id = ing2_res.json()["id"]

    return {"category_id": category_id, "ing1_id": ing1_id, "ing2_id": ing2_id}


@pytest.mark.asyncio
async def test_create_recipe_admin(admin_client, setup_recipe_data):
    data = setup_recipe_data
    payload = {
        "name": "Pasta Pomodoro",
        "description": "Simple pasta with tomato sauce",
        "category_id": data["category_id"],
        "cook_time_minutes": 20,
        "portions": 2,
        "difficulty": "easy",
        "ingredients": [
            {"ingredient_id": data["ing1_id"], "quantity": 200},
            {"ingredient_id": data["ing2_id"], "quantity": 100},
        ],
        "instructions": [
            {"step": 1, "description": "Boil pasta", "time_minutes": 10},
            {"step": 2, "description": "Add sauce", "time_minutes": 5},
        ],
    }
    response = await admin_client.post("/api/v1/recipes", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["name"] == payload["name"]
    assert res_data["total_calories"] > 0
    assert "id" in res_data


@pytest.mark.asyncio
async def test_get_recipes_list(user_client, admin_client, setup_recipe_data):
    data = setup_recipe_data
    payload = {
        "name": "Recipe for List",
        "description": "Test",
        "category_id": data["category_id"],
        "cook_time_minutes": 10,
        "portions": 1,
        "ingredients": [
            {"ingredient_id": data["ing1_id"], "quantity": 100},
            {"ingredient_id": data["ing2_id"], "quantity": 50},
        ],
        "instructions": [{"step": 1, "description": "Eat"}],
    }
    await admin_client.post("/api/v1/recipes", json=payload)

    response = await user_client.get("/api/v1/recipes")
    assert response.status_code == 200
    res_data = response.json()
    assert "data" in res_data
    assert len(res_data["data"]) >= 1
