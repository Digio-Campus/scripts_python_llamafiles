from openai import OpenAI

client1 = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")
client2 = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")

message = "¿Qué música te gusta?"

while True:
    messages1 = [{"role": "system", "content": "Eres un modelo de chat. Responde a este mensaje."},
                 {"role": "user", "content": message}]
    completion1 = client1.chat.completions.create(model="LLaMA_CPP", messages=messages1)

    response1 = completion1.choices[0].message.content
    print("AI 1: ", response1)


    messages2 = [{"role": "system", "content": "Eres un modelo de chat. Responde a este mensaje."},
                 {"role": "user", "content": response1}]

    completion2 = client2.chat.completions.create(model="LLaMA_CPP", messages=messages2)
    response2 = completion2.choices[0].message.content
    print("AI 2: ", response2)

    message = response2
