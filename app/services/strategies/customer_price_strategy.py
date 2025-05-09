from database.product_repository import ProductRepository
from database.connection import DBConnection
from .base_strategy import BaseStrategy
from utils.response_formatter import format_grouped_product_packages
class CustomerPriceStrategy(BaseStrategy):
    def handle(self, user_input):
        conn = DBConnection.get_instance()
        repo = ProductRepository(conn)
        packages = repo.get_package_by_name(user_input)
        return format_grouped_product_packages(packages)