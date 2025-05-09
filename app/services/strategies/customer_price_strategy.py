from database.product_repository import ProductRepository
from database.connection import DBConnection
from .base_strategy import BaseStrategy

class CustomerPriceStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        products = repo.get_product_by_name(user_input)
        return [
            f"{p['name']} hiện có giá gốc là {p['price']} VNĐ, khuyến mãi {p['price']/p['discount_price']*100} % ,giá khuyến mãi là {p['discount_price']} VNĐ"
            for p in products
        ]
