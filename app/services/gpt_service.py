from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ChatGPTService:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def get_response(self, prompt: str, system_prompt: str = None) -> str:
        """
        Gọi API GPT để tạo câu trả lời
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=150  # Giới hạn token để tiết kiệm chi phí
        )
        return response.choices[0].message.content.strip() 