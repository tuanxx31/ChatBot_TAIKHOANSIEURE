import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                database=os.getenv('MYSQL_DB', 'chatbot_db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', '')
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            
    def query_data(self, intent: str, user_input: str) -> dict:
        """
        Truy vấn dữ liệu dựa trên intent và câu hỏi
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Query khác nhau cho từng intent
            if intent == 'price':
                query = "SELECT name, price FROM products WHERE name LIKE %s"
                cursor.execute(query, (f"%{user_input}%",))
            elif intent == 'description':
                query = "SELECT name, description FROM products WHERE name LIKE %s"
                cursor.execute(query, (f"%{user_input}%",))
            elif intent == 'availability':
                query = "SELECT name, availability FROM products WHERE name LIKE %s"
                cursor.execute(query, (f"%{user_input}%",))
            else:
                query = "SELECT * FROM products WHERE name LIKE %s"
                cursor.execute(query, (f"%{user_input}%",))
                
            result = cursor.fetchall()
            cursor.close()
            return result
            
        except Error as e:
            print(f"Error querying data: {e}")
            return []
            
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

