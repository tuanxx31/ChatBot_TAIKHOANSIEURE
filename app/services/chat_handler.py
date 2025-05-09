from nlp.question_analyzer import QuestionAnalyzer
from services.gpt_service import ChatGPTService
from repositories.product_repository import ProductRepository
from services.strategies.response_strategy import CTVResponseStrategy, UserResponseStrategy
from services.strategies.store_info_strategy import StoreInfoStrategy
from services.strategies.hot_product_strategy import HotProductStrategy
from repositories.store_repository import StoreRepository
from repositories.hot_product_repository import HotProductRepository
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from collections import deque
import time

class ChatHandler:
    def __init__(self):
        # Core services
        self.product_repo = ProductRepository()
        self.question_analyzer = QuestionAnalyzer()
        self.chatgpt = ChatGPTService()
        
        # Cache configuration
        self.response_cache: Dict[str, str] = {}
        self.cache_expiry: Dict[str, datetime] = {}
        self.CACHE_DURATION = timedelta(hours=24)
        
        # Pattern cache configuration
        self.pattern_cache: Dict[str, str] = {}
        self.pattern_expiry: Dict[str, datetime] = {}
        self.PATTERN_CACHE_DURATION = timedelta(hours=12)
        
        # Rate limiting configuration
        self.request_times = deque(maxlen=500)  # 500 RPM limit
        self.token_count = 0
        self.last_token_reset = datetime.now()
        self.TOKEN_LIMIT = 200000  # 200k TPM limit
        self.TOKEN_RESET_INTERVAL = 60  # Reset every minute
        
        # Fix cứng role cho test
        self.user_role = "ctv"  # Có thể là "ctv" hoặc "user"
        
        # Initialize strategies with repositories
        self.response_strategy = self._get_response_strategy()
        self.store_strategy = StoreInfoStrategy(StoreRepository())
        self.hot_product_strategy = HotProductStrategy(HotProductRepository())
        
    def _get_response_strategy(self):
        """
        Lấy strategy phù hợp với role
        """
        if self.user_role == "ctv":
            return CTVResponseStrategy()
        return UserResponseStrategy()
        
    def _get_pattern_key(self, user_input: str) -> str:
        """
        Tạo pattern key từ câu hỏi
        """
        words_to_remove = ['là', 'có', 'được', 'không', 'của', 'và', 'hoặc', 'với']
        input_lower = user_input.lower()
        for word in words_to_remove:
            input_lower = input_lower.replace(f" {word} ", " ")
            
        words = input_lower.split()
        if len(words) <= 2:
            return input_lower
            
        important_words = [w for w in words if w not in words_to_remove][:3]
        return " ".join(important_words)
        
    def _find_similar_pattern(self, pattern_key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Tìm pattern tương tự trong cache
        """
        if pattern_key not in self.pattern_cache:
            return None, None
            
        if datetime.now() >= self.pattern_expiry[pattern_key]:
            del self.pattern_cache[pattern_key]
            del self.pattern_expiry[pattern_key]
            return None, None
            
        return pattern_key, self.pattern_cache[pattern_key]
        
    def _update_pattern_cache(self, pattern_key: str, response: str):
        """
        Cập nhật pattern cache
        """
        self.pattern_cache[pattern_key] = response
        self.pattern_expiry[pattern_key] = datetime.now() + self.PATTERN_CACHE_DURATION

    def handle_message(self, user_input: str) -> str:
        """
        Xử lý tin nhắn từ người dùng
        """
        # 1. Kiểm tra cache trực tiếp
        cache_key = self._generate_cache_key(user_input)
        if self._is_cache_valid(cache_key):
            return self.response_cache[cache_key]
            
        # 2. Kiểm tra pattern cache
        pattern_key = self._get_pattern_key(user_input)
        similar_pattern, cached_response = self._find_similar_pattern(pattern_key)
        if similar_pattern:
            return cached_response
            
        # 3. Phân tích câu hỏi
        analysis = self.question_analyzer.analyze_and_respond(user_input)
        
        # 4. Xử lý câu hỏi về thông tin cửa hàng
        if self._is_store_info_question(user_input):
            store_info = self.store_strategy.get_store_info()
            response = self.store_strategy.format_response(store_info)
            self._update_cache(cache_key, response)
            self._update_pattern_cache(pattern_key, response)
            return response
            
        # 5. Xử lý câu hỏi về sản phẩm hot
        if self._is_hot_product_question(user_input):
            hot_products = self.hot_product_strategy.get_hot_products()
            response = self.hot_product_strategy.format_response(hot_products)
            self._update_cache(cache_key, response)
            self._update_pattern_cache(pattern_key, response)
            return response
            
        # 6. Truy vấn database nếu có entity
        raw_data = None
        if analysis['entity_name']:
            raw_data = self._get_product_data(analysis)
            
        # 7. Tạo câu trả lời với dữ liệu đã có
        final_response = self._generate_response(user_input, analysis, raw_data)
        
        # 8. Lưu vào cache
        self._update_cache(cache_key, final_response)
        self._update_pattern_cache(pattern_key, final_response)
        
        return final_response

    def _is_store_info_question(self, user_input: str) -> bool:
        """
        Kiểm tra có phải câu hỏi về thông tin cửa hàng
        """
        keywords = ['cửa hàng', 'shop', 'store', 'liên hệ', 'địa chỉ']
        return any(keyword in user_input.lower() for keyword in keywords)
        
    def _is_hot_product_question(self, user_input: str) -> bool:
        """
        Kiểm tra có phải câu hỏi về sản phẩm hot
        """
        keywords = ['hot', 'bán chạy', 'nổi bật', 'phổ biến']
        return any(keyword in user_input.lower() for keyword in keywords)

    def _get_product_data(self, analysis: Dict) -> Optional[Dict]:
        """
        Lấy dữ liệu sản phẩm dựa trên intent
        """
        intent = analysis['intent']
        product_name = analysis['entity_name']
        
        if intent == "hỏi_gói_cước":
            return self.product_repo.get_product_package(product_name)
        elif intent == "hỏi_giá":
            return self.product_repo.get_product_price(product_name)
        else:
            return self.product_repo.get_product_by_name(product_name)

    def _check_rate_limits(self):
        """
        Kiểm tra và đợi nếu cần thiết để tuân thủ rate limits
        """
        current_time = datetime.now()
        
        # Reset token count if needed
        if (current_time - self.last_token_reset).seconds >= self.TOKEN_RESET_INTERVAL:
            self.token_count = 0
            self.last_token_reset = current_time
            
        # Check RPM limit
        if len(self.request_times) >= 500:
            oldest_request = self.request_times[0]
            if (current_time - oldest_request).seconds < 60:
                sleep_time = 60 - (current_time - oldest_request).seconds
                time.sleep(sleep_time)
                
        # Check TPM limit
        if self.token_count >= self.TOKEN_LIMIT:
            sleep_time = self.TOKEN_RESET_INTERVAL - (current_time - self.last_token_reset).seconds
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.token_count = 0
            self.last_token_reset = datetime.now()

    def _generate_response(self, user_input: str, analysis: Dict, raw_data: Optional[Dict]) -> str:
        """
        Tạo câu trả lời chuyên nghiệp bằng ChatGPT
        """
        try:
            # Kiểm tra rate limits
            self._check_rate_limits()
            
            user_prompt, system_prompt = self.response_strategy.format_response(user_input, analysis, raw_data)
            
            # Tối ưu prompt để giảm token và tránh cắt giữa chừng
            system_prompt = """
            Trả lời ngắn gọn, rõ ràng:
            1. Giới hạn 100-150 từ
            2. Chia thành 2-3 đoạn
            3. Kết thúc bằng "Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!"
            4. KHÔNG lặp lại câu kết thúc
            """
            
            # Ghi nhận request
            self.request_times.append(datetime.now())
            
            # Ước tính token
            estimated_tokens = len(user_prompt.split()) + len(system_prompt.split())
            self.token_count += estimated_tokens
            
            response = self.chatgpt.get_response(user_prompt, system_prompt)
            
            # Xử lý response
            response_text = self._process_response(response)
            
            return response_text
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau."
            
    def _process_response(self, response) -> str:
        """
        Xử lý response từ ChatGPT
        """
        if isinstance(response, str):
            response_text = response
        elif isinstance(response, dict):
            response_text = response.get('response', '')
        else:
            response_text = str(response)
            
        response_text = response_text.strip()
        
        # Loại bỏ câu kết thúc bị cắt giữa chừng
        end_phrases = ['Nếu cần th', 'Nếu cần thêm', 'hỗ trợ', 'giúp đỡ', 'tư vấn']
        for phrase in end_phrases:
            if phrase in response_text:
                response_text = response_text.split(phrase)[0].strip()
        
        # Loại bỏ câu kết thúc bị lặp lại
        if 'Nếu cần thêm thông tin' in response_text:
            response_text = response_text.split('Nếu cần thêm thông tin')[0].strip()
        
        # Thêm câu kết thúc hoàn chỉnh
        if not response_text.endswith(('.', '!', '?')):
            response_text += '.'
        response_text += ' Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!'
            
        return response_text

    def _generate_cache_key(self, user_input: str) -> str:
        """
        Tạo key cho cache từ câu hỏi và role
        """
        cache_input = f"{user_input.lower()}_{self.user_role}"
        return hashlib.md5(cache_input.encode()).hexdigest()

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
