#!/usr/bin/env python3
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8081/v1",
    api_key="sk-no-key-required"
)
completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "You are a weather and climate expert"},
        {"role": "user", "content": "I want to know about the weather in my city"}
    ]
)
print(completion.choices[0].message)
