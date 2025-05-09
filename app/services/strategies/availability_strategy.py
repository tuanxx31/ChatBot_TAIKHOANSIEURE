# services/strategies/availability_strategy.py

from database.product_repository import ProductRepository
from database.connection import DBConnection
from .base_strategy import BaseStrategy

class AvailabilityStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        products = repo.get_product_by_name(user_input)

        responses = []
        for p in products:
            stock_status = "còn hàng" if str(p["stock"]).lower() == "true" else "hết hàng"
            responses.append(f"Sản phẩm '{p['name']}' hiện đang {stock_status}.")
        return responses
