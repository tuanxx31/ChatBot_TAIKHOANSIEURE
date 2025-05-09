# app/services/strategies/description_strategy.py

from app.repositories.product_repository import ProductRepository
from database.connection import DBConnection
from services.strategies.base_strategy import BaseStrategy

class DescriptionStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        products = repo.get_product_by_name(user_input)
        return [
            f"Mô tả sản phẩm '{p['name']}' hiện chưa có thông tin mô tả chi tiết trong hệ thống."
            for p in products
        ]
