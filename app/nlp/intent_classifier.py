from services.chat_handler import ChatGPTService

class IntentClassifier:
    def __init__(self):
        self.labels = ["price", "description", "availability"]
        self.chatgpt = ChatGPTService()

    def classify(self, user_input: str) -> str:
        prompt = f"""Bạn là hệ thống phân loại câu hỏi chatbot.
Hãy xác định ý định (intent) của người dùng từ câu hỏi sau đây và chỉ trả về duy nhất một trong các nhãn sau: {", ".join(self.labels)}.

Câu hỏi: "{user_input}"
Intent:
"""
        response = self.chatgpt.get_response(prompt, system_prompt="Bạn là hệ thống phân loại ý định câu hỏi cho chatbot.")
        return response.lower().strip() if response in self.labels else "unknown"
