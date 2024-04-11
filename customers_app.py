import pandas as pd
from openai import OpenAI

data = pd.read_csv('~/Desktop/FCT/AppSheet/biostats.csv')

data_json = data.to_json(orient='records')

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key = "sk-no-key-required"
)

messages = [
    {"role": "system", "content": "Eres un experto en análisis de datos. Dime qué edad se repite más veces."},
    {"role": "user", "content": data_json}
]
print("data_json: ", data_json)

completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=messages
)

response = completion.choices[0].message.content
print("AI: ", response)
