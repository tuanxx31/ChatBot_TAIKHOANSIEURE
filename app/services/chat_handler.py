from openai import OpenAI
from config.settings import settings

class ChatGPTService:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.client = OpenAI()  # KHÔNG truyền api_key vào đây (vì dùng từ env)

    def get_response(self, prompt: str, system_prompt: str = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
