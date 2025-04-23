"""SUSE AI Kubernetes Operator Example
Author: Alessandro Festa
Email: <alessandro.festa1@suse.com>
"""
import os
from openai import OpenAI

client = OpenAI(
    base_url = "http://localhost:32434",
    api_key = os.environ["ollama"],
)

response = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "INSERT_INPUT_HERE",
                },
            ],
        },
    ],
    model = "qwen2.5:1.5b",
    max_tokens = 4096,
)

print(response.choices[0].message.content)