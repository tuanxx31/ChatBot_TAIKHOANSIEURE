from app.services.cache_service import CacheService
from app.services.response_service import ResponseService
from app.nlp.question_analyzer import QuestionAnalyzer
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.hot_product_repository import HotProductRepository
from app.services.strategies.response_strategy import CTVResponseStrategy
from app.services.strategies.store_info_strategy import StoreInfoStrategy
from app.services.strategies.hot_product_strategy import HotProductStrategy
import hashlib

class ChatHandler:
    def __init__(self):
        self.role = "ctv"
        self.question_analyzer = QuestionAnalyzer()
        self.product_repo = ProductRepository()
        self.response_strategy = CTVResponseStrategy()
        self.response_service = ResponseService(self.response_strategy)
        self.cache = CacheService()
        self.pattern_cache = CacheService(duration_hours=12)
        self.store_strategy = StoreInfoStrategy(StoreRepository())
        self.hot_product_strategy = HotProductStrategy(HotProductRepository())

    def handle_message(self, user_input: str) -> str:
        cache_key = self._generate_cache_key(user_input)
        # if self.cache.is_valid(cache_key):
        #     return self.cache.get(cache_key)

        pattern_key = self._get_pattern_key(user_input)
        # if self.pattern_cache.is_valid(pattern_key):
        #     return self.pattern_cache.get(pattern_key)

        if self._is_store_info(user_input):
            info = self.store_strategy.get_store_info()
            response = self.store_strategy.format_response(info)
        elif self._is_hot_product(user_input):
            hot = self.hot_product_strategy.get_hot_products()
            response = self.hot_product_strategy.format_response(hot)
        else:
            analysis = self.question_analyzer.analyze_and_respond(user_input)
            raw_data = self._get_product_data(analysis)
            response = self.response_service.generate_response(user_input, analysis, raw_data)

        self.cache.set(cache_key, response)
        self.pattern_cache.set(pattern_key, response)
        return response

    def _generate_cache_key(self, user_input: str) -> str:
        return hashlib.md5(f"{user_input.lower()}_{self.role}".encode()).hexdigest()

    def _get_pattern_key(self, user_input: str) -> str:
        words_to_remove = ['là', 'có', 'được', 'không', 'ở', 'của', 'và', 'hoặc', 'với']
        lowered = user_input.lower()
        for w in words_to_remove:
            lowered = lowered.replace(f" {w} ", " ")
        return " ".join(lowered.split()[:3])

    def _is_store_info(self, text: str) -> bool:
        return any(k in text.lower() for k in ['cửa hàng', 'shop', 'store', 'liên hệ', 'địa chỉ'])

    def _is_hot_product(self, text: str) -> bool:
        return any(k in text.lower() for k in ['hot', 'bán chạy', 'nổi bật', 'phổ biến'])

    def _get_product_data(self, analysis: dict):
        intent = analysis.get("intent")
        name = analysis.get("entity_name")
        if intent == "hỏi_gói_cước":
            return self.product_repo.get_product_package(name)
        elif intent == "hỏi_giá":
            return self.product_repo.get_product_price(name)
        return self.product_repo.get_product_by_name(name)
