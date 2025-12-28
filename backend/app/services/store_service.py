from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.db.mongodb import get_mongodb
from app.models.mongo.store_product import StoreProduct

class StoreService:
    def __init__(self):
        self.db = None
        self.collection = None

    async def _get_collection(self):
        if self.collection is None:
            self.db = await get_mongodb()
            self.collection = self.db.store_products
        return self.collection

    async def get_products_by_ingredient(self, ingredient_id: int) -> List[Dict[str, Any]]:
        collection = await self._get_collection()
        products = await collection.find({"ingredient_id": ingredient_id}).to_list(100)
        for product in products:
            product["id"] = str(product.pop("_id"))
        return products

    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        collection = await self._get_collection()
        result = await collection.insert_one(product_data)
        product = await collection.find_one({"_id": result.inserted_id})
        product["id"] = str(product.pop("_id"))
        return product

    async def get_all_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        collection = await self._get_collection()
        products = await collection.find().limit(limit).to_list(limit)
        for product in products:
            product["id"] = str(product.pop("_id"))
        return products

store_service = StoreService()
