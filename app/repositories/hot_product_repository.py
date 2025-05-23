from database.connection import get_db_connection
from repositories.interfaces.hot_product_repository_interface import HotProductRepositoryInterface
from typing import List, Dict

class HotProductRepository(HotProductRepositoryInterface):
    def __init__(self):
        self.db = get_db_connection()
        
    def get_hot_products(self) -> List[Dict]:
        """
        Lấy danh sách sản phẩm hot từ bảng top_selling_products
        """
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT p.* 
                FROM product p
                INNER JOIN top_selling_products t ON p.id = t.product_id
                WHERE p.is_active = 1
                ORDER BY t.id ASC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting hot products: {e}")
            return [] 