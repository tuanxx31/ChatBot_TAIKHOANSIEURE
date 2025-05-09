from database.connection import DatabaseConnection

class ProductRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_product_by_name(self, product_name: str) -> dict:
        """
        Lấy thông tin sản phẩm theo tên
        """
        return self.db.query_data(
            intent="hỏi_thông_tin",
            entity=product_name,
            entity_type="product"
        )
    
    def get_product_price(self, product_name: str) -> dict:
        """
        Lấy thông tin giá sản phẩm
        """
        return self.db.query_data(
            intent="hỏi_giá",
            entity=product_name,
            entity_type="product"
        )
    
    def get_product_package(self, product_name: str) -> dict:
        """
        Lấy thông tin gói cước sản phẩm
        """
        return self.db.query_data(
            intent="hỏi_gói_cước",
            entity=product_name,
            entity_type="product"
        ) 