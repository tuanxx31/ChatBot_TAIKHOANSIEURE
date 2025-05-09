class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_product_by_name(self, name):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT 
                name,
                JSON_EXTRACT(product_package, '$[0].price') AS price,
                JSON_EXTRACT(product_package, '$[0].discountPrice') AS discount_price,
                JSON_EXTRACT(product_package, '$[0].ctvPrice') AS ctv_price,
                JSON_EXTRACT(product_package, '$[0].stock') AS stock
            FROM product
            WHERE name LIKE %s
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()


