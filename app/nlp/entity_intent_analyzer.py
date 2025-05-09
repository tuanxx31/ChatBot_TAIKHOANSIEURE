import json
from services.chat_handler import ChatGPTService

class EntityIntentAnalyzer:
    def __init__(self):
        self.chatgpt = ChatGPTService()
        self.cache = {}

    def analyze(self, user_input: str) -> dict:
        if user_input in self.cache:
            return self.cache[user_input]

        prompt = f'''Hãy phân tích câu hỏi sau: "{user_input}"

Trả về kết quả dưới dạng JSON chỉ chứa 2 trường:
- "intent": một trong các giá trị "price", "description", "availability"
- "product": tên sản phẩm người dùng đang nhắc tới

Không thêm bất kỳ thông tin nào ngoài JSON.'''

        response = self.chatgpt.get_response(
            prompt,
            system_prompt="Bạn là hệ thống phân tích ý định và tên sản phẩm cho chatbot."
        )

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {"intent": "unknown", "product": user_input.strip()}

        self.cache[user_input] = result
        return result
