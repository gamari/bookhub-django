import openai, logging
from typing import List

logger = logging.getLogger("app_logger")

class OpenAiClient(object):
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key
        self.messages = []
    
    def reset(self):
        self.messages = []

    def add_system_message(self, content: str):
        self.messages.append({
            "role": "system",
            "content": content
        })

    def add_user_message(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_sample_message(self, role: str, content: str):
        """サンプルのメッセージを追加するメソッド。"""
        self.messages.append({
            "role": role,
            "content": content
        })

    def query(self, model="gpt-3.5-turbo", **kwargs):
        logger.debug(f"messages: {self.messages}")
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.messages,
            **kwargs
        )
        tokens = response["usage"]["total_tokens"]
        logger.debug(f"tokens: {tokens}")
        return response.choices[0].message.content

