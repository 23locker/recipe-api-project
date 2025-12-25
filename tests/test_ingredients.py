import pytest


@pytest.fixture
async def category_id(admin_client):
    payload = {"name": "Test Category"}
    res = await admin_client.post("/api/v1/category", json=payload)
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_ingredient_admin(admin_client, category_id):
    payload = {
        "name": "Chicken Breast",
        "calories_per_100g": 165.0,
        "protein_per_100g": 31.0,
        "fat_per_100g": 3.6,
        "carbs_per_100g": 0.0,
        "category_id": category_id,
    }
    response = await admin_client.post("/api/v1/ingredients", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["category_id"] == category_id


@pytest.mark.asyncio
async def test_get_ingredients_list(user_client, admin_client, category_id):
    await admin_client.post(
        "/api/v1/ingredients",
        json={
            "name": "Milk",
            "calories_per_100g": 42,
            "protein_per_100g": 3.4,
            "fat_per_100g": 1.0,
            "carbs_per_100g": 5.0,
            "category_id": category_id,
        },
    )

    response = await user_client.get("/api/v1/ingredients")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 1


@pytest.mark.asyncio
async def test_substitute_logic(admin_client, user_client, category_id):
    ing1_res = await admin_client.post(
        "/api/v1/ingredients",
        json={
            "name": "Butter",
            "calories_per_100g": 717,
            "protein_per_100g": 0.8,
            "fat_per_100g": 81,
            "carbs_per_100g": 0.1,
            "category_id": category_id,
        },
    )
    ing1_id = ing1_res.json()["id"]

    ing2_res = await admin_client.post(
        "/api/v1/ingredients",
        json={
            "name": "Margarine",
            "calories_per_100g": 717,
            "protein_per_100g": 0.2,
            "fat_per_100g": 80,
            "carbs_per_100g": 0.1,
            "category_id": category_id,
        },
    )
    ing2_id = ing2_res.json()["id"]

    sub_payload = {
        "original_ingredient_id": ing1_id,
        "substitute_ingredient_id": ing2_id,
        "coefficient": 1.0,
    }
    sub_res = await admin_client.post(
        "/api/v1/ingredients/substitutes", json=sub_payload
    )
    assert sub_res.status_code == 200

    get_sub_res = await user_client.get(f"/api/v1/ingredients/{ing1_id}/substitutes")
    assert get_sub_res.status_code == 200
    subs = get_sub_res.json()
    assert len(subs) >= 1
    assert subs[0]["substitute_ingredient_id"] == ing2_id
