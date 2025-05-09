from database.product_repository import ProductRepository
from database.connection import DBConnection
from .base_strategy import BaseStrategy

class CtvPriceStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        products = repo.get_product_by_name(user_input)
        print(products)
        return [
            f"{p['name']} có giá dành cho cộng tác viên là {p['ctv_price']} VNĐ"
            for p in products
        ]
