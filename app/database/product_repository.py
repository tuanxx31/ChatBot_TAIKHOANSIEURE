class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_product_by_name(self, name):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT 
                JSON_UNQUOTE(JSON_EXTRACT(productPackage, '$[0].name')) AS name,
                JSON_EXTRACT(productPackage, '$[0].price') AS price,
                JSON_EXTRACT(productPackage, '$[0].discountPrice') AS discount_price,
                JSON_EXTRACT(productPackage, '$[0].ctvPrice') AS ctv_price,
                JSON_EXTRACT(productPackage, '$[0].stock') AS stock
            FROM product
            WHERE JSON_UNQUOTE(JSON_EXTRACT(productPackage, '$[0].name')) LIKE %s
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()


