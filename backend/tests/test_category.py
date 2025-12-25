import pytest


@pytest.mark.asyncio
async def test_create_category_admin(admin_client):
    payload = {"name": "Breakfast", "description": "Morning meals"}
    response = await admin_client.post("/api/v1/category", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert "id" in data


@pytest.mark.asyncio
async def test_create_category_user_forbidden(user_client):
    payload = {"name": "Lunch", "description": "Afternoon meals"}
    response = await user_client.post("/api/v1/category", json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_category_success(client, admin_client):
    payload = {"name": "Dinner"}
    create_res = await admin_client.post("/api/v1/category", json=payload)
    category_id = create_res.json()["id"]

    response = await client.get(f"/api/v1/category/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Dinner"


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    response = await client.get("/api/v1/category/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_admin(admin_client):
    payload = {"name": "Snack"}
    create_res = await admin_client.post("/api/v1/category", json=payload)
    category_id = create_res.json()["id"]

    response = await admin_client.delete(f"/api/v1/category/{category_id}")
    assert response.status_code == 204

    get_res = await admin_client.get(f"/api/v1/category/{category_id}")
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_user_forbidden(user_client, admin_client):
    payload = {"name": "Snack"}
    create_res = await admin_client.post("/api/v1/category", json=payload)
    category_id = create_res.json()["id"]

    response = await user_client.delete(f"/api/v1/category/{category_id}")
    assert response.status_code == 403
