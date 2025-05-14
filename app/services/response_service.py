from app.services.gpt_service import ChatGPTService
from app.services.rate_limiter import RateLimiter

class ResponseService:
    def __init__(self, strategy):
        self.chatgpt = ChatGPTService()
        self.ratelimiter = RateLimiter()
        self.strategy = strategy

    def generate_response(self, user_input: str, analysis: dict, raw_data: dict = None) -> str:
        try:
            user_prompt, system_prompt = self.strategy.format_response(user_input, analysis, raw_data)
            system_prompt = """
            Trả lời ngắn gọn, rõ ràng:
            1. Giới hạn 100-150 từ
            2. Chia thành 2-3 đoạn
            3. Kết thúc bằng \"Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!\"
            """
            estimated_tokens = len(user_prompt.split()) + len(system_prompt.split())
            self.ratelimiter.check(estimated_tokens)
            raw_response = self.chatgpt.get_response(user_prompt, system_prompt)
            return self._clean_response(raw_response)
        except Exception as e:
            print(f"[ERROR] GPT Response: {e}")
            return "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau."

    def _clean_response(self, response) -> str:
        text = response.get("response") if isinstance(response, dict) else str(response)
        text = text.strip().split("Nếu cần thêm")[0].strip()
        if not text.endswith(('.', '!', '?')):
            text += '.'
        return text + ' Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết nhé!'
