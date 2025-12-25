import pytest

@pytest.mark.asyncio
async def test_parse_stores_admin(admin_client):
    response = await admin_client.post("/api/v1/admin/parse-stores")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_parse_stores_user_forbidden(user_client):
    response = await user_client.post("/api/v1/admin/parse-stores")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_stats_admin(admin_client):
    response = await admin_client.get("/api/v1/admin/stats")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_get_stats_user_forbidden(user_client):
    response = await user_client.get("/api/v1/admin/stats")
    assert response.status_code == 403
