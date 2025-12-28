from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models.tortoise.user import User
from app.services.store_service import store_service

router = APIRouter(tags=["store"])

@router.get("/products/{ingredient_id}")
async def get_ingredient_prices(
    ingredient_id: int, 
    current_user: User = Depends(get_current_user)
):
    """Получить цены на ингредиент в магазинах"""
    products = await store_service.get_products_by_ingredient(ingredient_id)
    return products

@router.get("/products")
async def get_all_store_products(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """Получить список всех товаров в магазинах"""
    return await store_service.get_all_products(limit)
