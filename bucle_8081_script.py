#!/usr/bin/env python3
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8081/v1",
    api_key = "sk-no-key-required"
)

messages = [
    {"role": "system", "content": "You are an AI assistant."},
]

while True:
    user_input = input("You: ")

    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="LLaMA_CPP", # El nombre del modelo
        messages=messages
    )

    response = completion.choices[0].message.content
    print("AI: ", response)

    messages.append({"role": "assistant", "content": response})
