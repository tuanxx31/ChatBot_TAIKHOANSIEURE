import openai
from config.settings import settings

class ChatGPTService:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        openai.api_key = settings.OPENAI_API_KEY

    def get_response(self, prompt: str, system_prompt: str = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
