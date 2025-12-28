import asyncio
import sys

import httpx

BASE_URL = "http://localhost:8000/api/v1"


# Helper to print colored status
def print_status(msg, success=True):
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{msg}{reset}")


async def get_token():
    async with httpx.AsyncClient() as client:
        email = f"admin_test_{sys.maxsize}@example.com"
        password = "secretpassword"
        payload = {
            "email": email,
            "password": password,
            "full_name": "Test Admin",
            "is_admin": True,
        }

        try:
            reg_res = await client.post(f"{BASE_URL}/auth/register", json=payload)
            if reg_res.status_code == 201:
                print("Registered new user")
        except Exception as e:
            pass

        from httpx import AsyncClient

        login_client = AsyncClient()
        login_res = await login_client.post(
            f"{BASE_URL}/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        await login_client.aclose()
        if login_res.status_code != 200:
            print_status(f"Login failed: {login_res.text}", False)
            return None

        return login_res.json()["access_token"]


async def verify_crud():
    print("Starting CRUD verification...")

    token = await get_token()
    if not token:
        print_status(
            "Skipping tests due to auth failure (maybe need manual admin creation)",
            False,
        )
        return

    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(headers=headers, base_url=BASE_URL) as client:
        print("\n--- Testing INGREDIENTS ---")

        ing_payload = {
            "name": "Test Ingredient CRUD",
            "calories_per_100g": 100,
            "protein_per_100g": 10,
            "fat_per_100g": 10,
            "carbs_per_100g": 10,
            "category_id": 1,
        }

        try:
            cat_payload = {"name": "Test Category"}
            cat_res = await client.post("/category", json=cat_payload)
            if cat_res.status_code in [200, 201]:
                cat_id = cat_res.json()["id"]
                ing_payload["category_id"] = cat_id
                print_status("Category created", True)
            else:
                print_status(f"Category creation failed: {cat_res.text}", False)
                cats = await client.get("/category")
                if cats.json().get("items"):
                    ing_payload["category_id"] = cats.json()["items"][0]["id"]
                else:
                    return
        except Exception as e:
            print_status(f"Category error: {e}", False)

        res = await client.post("/ingredients", json=ing_payload)
        if res.status_code in [200, 201]:
            ing_data = res.json()
            ing_id = ing_data["id"]
            print_status(f"Ingredient created: {ing_id}", True)
        else:
            print_status(f"Ingredient creation failed: {res.text}", False)
            return

        update_payload = ing_payload.copy()
        update_payload["name"] = "Updated Ingredient Name"
        res = await client.put(f"/ingredients/{ing_id}", json=update_payload)
        if res.status_code == 200 and res.json()["name"] == "Updated Ingredient Name":
            print_status("Ingredient updated", True)
        else:
            print_status(f"Ingredient update failed: {res.text}", False)

        res = await client.delete(f"/ingredients/{ing_id}")
        if res.status_code == 204:
            print_status("Ingredient deleted", True)
        else:
            print_status(f"Ingredient delete failed: {res.text}", False)

        print("\n--- Testing RECIPES ---")

        ing1_res = await client.post(
            "/ingredients", json={**ing_payload, "name": "Ing 1"}
        )
        ing2_res = await client.post(
            "/ingredients", json={**ing_payload, "name": "Ing 2"}
        )

        if ing1_res.status_code not in [200, 201] or ing2_res.status_code not in [
            200,
            201,
        ]:
            print_status("Failed to create setup ingredients", False)
            return

        ing1_id = ing1_res.json()["id"]
        ing2_id = ing2_res.json()["id"]

        recipe_payload = {
            "name": "Test Recipe CRUD",
            "description": "Desc",
            "category_id": ing_payload["category_id"],
            "cook_time_minutes": 30,
            "portions": 2,
            "difficulty": "easy",
            "ingredients": [
                {"ingredient_id": ing1_id, "quantity": 100, "unit": "g"},
                {"ingredient_id": ing2_id, "quantity": 200, "unit": "g"},
            ],
            "instructions": [{"step": 1, "description": "Step 1", "time_minutes": 10}],
        }

        res = await client.post("/recipes", json=recipe_payload)
        if res.status_code in [200, 201]:
            rec_data = res.json()
            rec_id = rec_data["id"]
            print_status(f"Recipe created: {rec_id}", True)
        else:
            print_status(f"Recipe creation failed: {res.text}", False)
            return

        recipe_payload["name"] = "Updated Recipe Name"
        res = await client.put(f"/recipes/{rec_id}", json=recipe_payload)
        if res.status_code == 200 and res.json()["name"] == "Updated Recipe Name":
            print_status("Recipe updated", True)
        else:
            print_status(f"Recipe update failed: {res.text}", False)

        res = await client.delete(f"/recipes/{rec_id}")
        if res.status_code == 204:
            print_status("Recipe deleted", True)
        else:
            print_status(f"Recipe delete failed: {res.text}", False)


if __name__ == "__main__":
    asyncio.run(verify_crud())
