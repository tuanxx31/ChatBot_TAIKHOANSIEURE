import json


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
    def get_package_by_name(self, keyword):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT name, product_package FROM product WHERE name LIKE %s"
        cursor.execute(query, (f"%{keyword}%",))
        raw = cursor.fetchall()

        result = []
        for row in raw:
            try:
                packages = json.loads(row["product_package"])
                for p in packages:
                    # keyword có thể là "capcut" hoặc "premium"
                    if keyword.lower() in p["name"].lower() or keyword.lower() in row["name"].lower():
                        p["product_name"] = row["name"]
                        result.append(p)
            except Exception:
                continue
        return result


