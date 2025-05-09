from repositories.interfaces.store_repository_interface import StoreRepositoryInterface
from typing import Dict

class StoreInfoStrategy:
    def __init__(self, store_repository: StoreRepositoryInterface):
        self.store_repo = store_repository
        
    def get_store_info(self) -> Dict:
        """
        Lấy thông tin cửa hàng
        """
        try:
            config = self.store_repo.get_store_config()
            if not config:
                return self._get_default_store_info()
                
            return {
                "name": config.get('name_web', 'TAIKHOANSIEURE.VN'),
                "description": config.get('description', 'Chuyên cung cấp tài khoản bản quyền giá rẻ'),
                "contact": {
                    "phone": config.get('number_phone', '0396891837'),
                    "email": config.get('email_contact', 'baolamh775@gmail.com'),
                    "zalo": config.get('zalo', 'https://zalo.me/0396891837'),
                    "facebook": config.get('facebook_link', 'https://www.facebook.com/hoang.bao.lam.941795/'),
                    "telegram": f"https://t.me/{config.get('telegram_chat_id', '5151817215')}"
                },
                "address": config.get('address', '64 đường 5, KP.4, P.Linh Xuân, Q. Thủ Đức'),
                "notice": config.get('topbar_notice_content', '')
            }
        except Exception as e:
            print(f"Error getting store info: {e}")
            return self._get_default_store_info()
            
    def _get_default_store_info(self) -> Dict:
        """
        Thông tin cửa hàng mặc định nếu không lấy được từ database
        """
        return {
            "name": "TAIKHOANSIEURE.VN",
            "description": "Chuyên cung cấp tài khoản bản quyền giá rẻ",
            "contact": {
                "phone": "0396891837",
                "email": "baolamh775@gmail.com",
                "zalo": "https://zalo.me/0396891837",
                "facebook": "https://www.facebook.com/hoang.bao.lam.941795/",
                "telegram": "https://t.me/5151817215"
            },
            "address": "64 đường 5, KP.4, P.Linh Xuân, Q. Thủ Đức",
            "notice": "Các đại lý cần giá sỉ tất cả các mặt hàng uy tín - chất lượng - lịch sự. Đăng ký lấy hàng gửi gmail về cho shop qua zalo 0396891837. Shop xin cảm ơn!"
        }
        
    def format_response(self, store_info: Dict) -> str:
        """
        Định dạng thông tin cửa hàng
        """
        response = f"""
🏪 {store_info['name']}
{store_info['description']}

📞 Liên hệ:
- Điện thoại: {store_info['contact']['phone']}
- Email: {store_info['contact']['email']}
- Zalo: {store_info['contact']['zalo']}
- Facebook: {store_info['contact']['facebook']}
- Telegram: {store_info['contact']['telegram']}

📍 Địa chỉ: {store_info['address']}
"""

        # Thêm thông báo nếu có
        if store_info.get('notice'):
            response += f"\n📢 Thông báo: {store_info['notice']}"
            
        response += "\n\nNếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!"
        return response 