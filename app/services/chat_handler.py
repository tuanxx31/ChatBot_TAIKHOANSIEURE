from nlp.intent_analyzer import IntentAnalyzer
from database.connection import DatabaseConnection
from nlp.natural_response_service import NaturalResponseService
import hashlib
import json

class ChatHandler:
    def __init__(self):
        self.db = DatabaseConnection()
        self.intent_analyzer = IntentAnalyzer()
        self.natural_response = NaturalResponseService()
        self.response_cache = {}
        
    def handle_message(self, user_input: str) -> str:
        """
        Xử lý tin nhắn từ người dùng
        """
        # 1. Kiểm tra cache
        cache_key = self._generate_cache_key(user_input)
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
            
        # 2. Phân tích intent (không dùng GPT)
        intent = self.intent_analyzer.analyze(user_input)
        
        # 3. Truy vấn database
        raw_data = self.db.query_data(intent, user_input)
        
        if not raw_data:
            return "Xin lỗi, tôi không tìm thấy thông tin về sản phẩm này."
            
        # 4. Tạo câu trả lời tự nhiên bằng GPT
        response = self.natural_response.from_data(json.dumps(raw_data, ensure_ascii=False))
        
        # 5. Lưu vào cache
        self.response_cache[cache_key] = response
        
        return response
        
    def _generate_cache_key(self, user_input: str) -> str:
        """
        Tạo key cho cache từ câu hỏi
        """
        return hashlib.md5(user_input.lower().encode()).hexdigest()
        
    def clear_cache(self):
        """
        Xóa cache khi cần
        """
        self.response_cache.clear()
