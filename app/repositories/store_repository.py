from database.connection import get_db_connection
from repositories.interfaces.store_repository_interface import StoreRepositoryInterface
from typing import Optional, Dict

class StoreRepository(StoreRepositoryInterface):
    def __init__(self):
        self.db = get_db_connection()
        
    def get_store_config(self) -> Optional[Dict]:
        """
        Lấy thông tin cửa hàng từ bảng configs
        """
        try:
            query = """
                SELECT name_web, description, number_phone, email_contact, 
                       zalo, facebook_link, address, topbar_notice_content,
                       telegram_chat_id
                FROM configs 
                LIMIT 1
            """
            result = self.db.execute(query).fetchone()
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error getting store config: {e}")
            return None 