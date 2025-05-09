from repositories.interfaces.hot_product_repository_interface import HotProductRepositoryInterface
from typing import List, Dict

class HotProductStrategy:
    def __init__(self, hot_product_repository: HotProductRepositoryInterface):
        self.hot_product_repo = hot_product_repository
        
    def get_hot_products(self) -> List[Dict]:
        """
        Lấy danh sách sản phẩm hot
        """
        try:
            return self.hot_product_repo.get_hot_products()
        except Exception as e:
            print(f"Error getting hot products: {e}")
            return []
            
    def format_response(self, products: List[Dict]) -> str:
        """
        Định dạng danh sách sản phẩm hot
        """
        if not products:
            return "Hiện tại chưa có sản phẩm hot nào."
            
        response = "🔥 Sản phẩm hot:\n\n"
        
        for product in products:
            response += f"📦 {product['name']}\n"
            response += f"💰 Giá: {product.get('price', 'Liên hệ')}\n"
            if product.get('description'):
                response += f"📝 {product['description'][:100]}...\n"
            response += "\n"
            
        response += "Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!"
        return response 