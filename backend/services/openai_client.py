import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self, client=None):
        self.client = client

    def get(self):
        if self.client is None:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE_URL"),
            )
        return self.client


openai_client = OpenAIClient()
