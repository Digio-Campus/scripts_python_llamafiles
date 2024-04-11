import requests
from openai import OpenAI

city = input("Por favor, introduce el nombre de tu ciudad: ")

response = requests.get(
    f"https://api.weatherapi.com/v1/current.json?key=ef06cadcf2e34b8fb0f211843240604&q={city}&aqi=no")

if response.status_code == 200:
    weather_data = response.json()
    condition = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']

    client = OpenAI(
        base_url="http://127.0.0.1:8080/v1",
        api_key="sk-no-key-required"
    )

    messages = [
        {"role": "system", "content": "Eres un experto en clima y meteorología."},
        {"role": "user", "content": f" Quiero que me hagas una explicación en lenguaje natural sobre cómo es el clima "
                                    f"en {city}. Ten en cuenta que ahora mismo es {condition} con temperatura "
                                    f"de {temperature} grados Celsius."}
    ]

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=messages
    )

    response = completion.choices[0].message.content
    print("AI: ", response)
else:
    print("Hubo un error al obtener los datos del clima. Por favor, intenta de nuevo.")
