import json


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_product_by_name(self, name):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT 
                id,
                name,
                description,
                detail_information,
                product_package,
                type,
                is_active,
                is_payment_before,
                star,
                thumbnail,
                tick_tag
            FROM product
            WHERE name LIKE %s AND is_active = 1
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()

    def get_package_by_name(self, keyword):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT 
                id,
                name,
                description,
                product_package,
                type,
                is_active
            FROM product 
            WHERE (name LIKE %s OR description LIKE %s) 
            AND is_active = 1
        """
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        raw = cursor.fetchall()

        result = []
        for row in raw:
            try:
                packages = json.loads(row["product_package"])
                for p in packages:
                    if keyword.lower() in p["name"].lower() or keyword.lower() in row["name"].lower():
                        p["product_name"] = row["name"]
                        p["product_description"] = row["description"]
                        p["product_type"] = row["type"]
                        result.append(p)
            except Exception:
                continue
        return result

    def get_all_active_products(self):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT 
                id,
                name,
                description,
                product_package,
                type,
                is_active
            FROM product
            WHERE is_active = 1
        """
        cursor.execute(query)
        return cursor.fetchall()


