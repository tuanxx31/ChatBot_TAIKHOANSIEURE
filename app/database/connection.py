import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_db_connection():
    """
    Tạo và trả về kết nối database
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'chatbot_db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'chatbot_db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '')
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            
    def query_data(self, intent: str, entity: str, entity_type: str = 'product') -> dict:
        """
        Truy vấn dữ liệu dựa trên intent và entity
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if entity_type == 'product':
                # Query thông tin sản phẩm
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
                cursor.execute(query, (f"%{entity}%",))
                result = cursor.fetchone()
                
                if result:
                    # Parse product_package JSON
                    if result['product_package']:
                        result['product_package'] = json.loads(result['product_package'])
                    else:
                        result['product_package'] = []
                        
                    return result
                return None
                
            return None
            
        except Error as e:
            print(f"Error querying data: {e}")
            return None
            
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

