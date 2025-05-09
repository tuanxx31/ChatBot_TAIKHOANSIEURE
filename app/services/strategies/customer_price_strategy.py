from database.product_repository import ProductRepository
from database.connection import DBConnection
from .base_strategy import BaseStrategy

class CustomerPriceStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        products = repo.get_product_by_name(user_input)
        result = []

        for p in products:
            name = p["name"]
            price = float(p["price"])
            discount = float(p["discount_price"])

            if discount and discount < price:
                percent = round((1 - discount / price) * 100)
                text = f"{name} hiện có giá gốc {price:.0f} VNĐ, khuyến mãi {percent}% còn {discount:.0f} VNĐ"
            else:
                text = f"{name} hiện có giá {price:.0f} VNĐ (không có khuyến mãi)"
            result.append(text)

        return result
