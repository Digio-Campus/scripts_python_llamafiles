import requests
from openai import OpenAI


def get_city_name():
    sentence = input("Introduce una frase: ")
    client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")
    messages = [{"role": "system",
                 "content": "Responde solo con el nombre de la ciudad que se menciona en la siguiente frase."},
                {"role": "user", "content": sentence}]
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages)
    return completion.choices[0].message.content


def get_weather(city):
    response = requests.get(
        f"https://api.weatherapi.com/v1/current.json?key=ef06cadcf2e34b8fb0f211843240604&q={city}&aqi=no")
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data['current']['condition']['text'], weather_data['current']['temp_c']
    else:
        return None, None


def translate_weather_to_spanish(weather_in_english):
    client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")
    messages = [{"role": "system",
                 "content": "Eres un modelo de lenguaje que puede traducir el clima de inglés a español."},
                {"role": "user", "content": weather_in_english}]
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages)
    return completion.choices[0].message.content


def get_weather_explanation(city, condition, temperature):
    client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")
    messages = [{"role": "system",
                 "content": "Eres un experto en meteorología y clima. Genera una explicación basada en la siguiente "
                            "información."},
                {"role": "user",
                 "content": f"La ciudad es {city}, el clima es {condition}, y la temperatura es de {temperature} grados Celsius."}]
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages)
    return completion.choices[0].message.content


city = get_city_name()
print("La ciudad es ", city)
condition, temperature = get_weather(city)
print("El clima en inglés es", condition, "y la temperatura es", temperature)
condition = translate_weather_to_spanish(condition)
print("El clima en español es", condition)
if condition and temperature:
    explanation = get_weather_explanation(city, condition, temperature)
    print("Explicación: ", explanation)
else:
    print("Hubo un error al obtener los datos del clima. Por favor, intenta de nuevo.")
