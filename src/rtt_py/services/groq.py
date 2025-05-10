import os

import requests
import json

from typing import TypedDict


class InputMessage(TypedDict):
    context: str
    query: str


class ChatCompletions:
    """
    Class to handle chat completions using the Groq API.
    """

    def __init__(self):
        """
        Initialize the ChatCompletions class with the provided API key.

        :param api_key: The API key for authentication with the Groq API.
        """

        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.model = "llama-3.3-70b-versatile"

    def _embed_context(self, context: str) -> str:
        """
        Embed the context into the message.

        :param context: The context to embed.
        :return: The embedded context.
        """
        return f"""
        <context>
            {context}
        </context>

        YOUR TASK IS TO ANSWER THE QUESTIONS BASED ON THE CONTEXT ABOVE.
        """

    def generate_response(self, messages: InputMessage) -> tuple[str, int, int]:
        """
        Generate a response from the Groq API based on the provided messages.

        :param messages: The messages to send to the Groq API.
        :return: A tuple containing the response text, input token , and output tokens.

        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": messages["query"]},
                {"role": "system", "content": self._embed_context(messages["context"])},
            ],
        }

        response = requests.post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        response.raise_for_status()

        return (
            response.json()["choices"][0]["message"]["content"],
            response.json()["usage"]["prompt_tokens"],
            response.json()["usage"]["completion_tokens"],
        )
