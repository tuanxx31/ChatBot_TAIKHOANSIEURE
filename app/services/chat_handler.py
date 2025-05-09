from nlp.question_analyzer import QuestionAnalyzer
from database.connection import DatabaseConnection
from services.gpt_service import ChatGPTService
import hashlib
import json
from datetime import datetime, timedelta

class ChatHandler:
    def __init__(self):
        self.db = DatabaseConnection()
        self.question_analyzer = QuestionAnalyzer()
        self.chatgpt = ChatGPTService()
        self.response_cache = {}
        self.cache_expiry = {}  # Thêm cache expiry
        self.CACHE_DURATION = timedelta(hours=24)  # Cache trong 24 giờ
        
    def handle_message(self, user_input: str) -> str:
        """
        Xử lý tin nhắn từ người dùng
        """
        # 1. Kiểm tra cache
        cache_key = self._generate_cache_key(user_input)
        if self._is_cache_valid(cache_key):
            return self.response_cache[cache_key]
            
        # 2. Phân tích câu hỏi để lấy thông tin cơ bản
        analysis = self.question_analyzer.analyze_and_respond(user_input)
        
        # 3. Truy vấn database nếu có entity
        raw_data = None
        if analysis['entity_name']:
            raw_data = self.db.query_data(
                analysis['intent'], 
                analysis['entity_name'], 
                analysis['entity_type']
            )
            
        # 4. Tạo câu trả lời với dữ liệu đã có
        final_response = self._generate_response(user_input, analysis, raw_data)
        
        # 5. Lưu vào cache với thời gian hết hạn
        self._update_cache(cache_key, final_response)
        
        return final_response

    def _generate_response(self, user_input: str, analysis: dict, raw_data: dict) -> str:
        """
        Tạo câu trả lời chuyên nghiệp bằng ChatGPT
        """
        if not raw_data:
            return "Xin lỗi, tôi không tìm thấy thông tin về sản phẩm này."

        # Chuẩn bị prompt cho ChatGPT - tối ưu hóa để ngắn gọn hơn
        system_prompt = """Bạn là nhân viên tư vấn. Trả lời tự nhiên, thân thiện bằng tiếng Việt. 
        Trình bày rõ ràng, thêm thông tin hữu ích và sẵn sàng hỗ trợ thêm."""

        # Format dữ liệu sản phẩm - chỉ lấy thông tin cần thiết
        product_info = {
            "tên": raw_data['name'],
            "mô_tả": raw_data['description'],
            "gói_cước": raw_data['product_package']
        }

        # Tối ưu user prompt
        user_prompt = f"Khách hỏi: {user_input}\nThông tin: {json.dumps(product_info, ensure_ascii=False)}"

        try:
            response = self.chatgpt.get_response(user_prompt, system_prompt)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau."
        
    def _generate_cache_key(self, user_input: str) -> str:
        """
        Tạo key cho cache từ câu hỏi
        """
        return hashlib.md5(user_input.lower().encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """
        Kiểm tra cache còn hạn không
        """
        if cache_key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[cache_key]

    def _update_cache(self, cache_key: str, response: str):
        """
        Cập nhật cache với thời gian hết hạn
        """
        self.response_cache[cache_key] = response
        self.cache_expiry[cache_key] = datetime.now() + self.CACHE_DURATION
        
    def clear_cache(self):
        """
        Xóa cache khi cần
        """
        self.response_cache.clear()
        self.cache_expiry.clear()
