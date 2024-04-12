from openai import OpenAI
import mysql.connector

model = "Rocket 3-B"
temp = 1.0
print("\nModelo: ", model)
print("\nTemperatura: ", temp)

conexion = mysql.connector.connect(host="localhost", user="juan", password="mysqljuan", database="llamafiles")
cursor = conexion.cursor()

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-no-key-required"
)
first_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "I want you to invent a story between 100 and 120 words long."},
    ],
    temperature=temp,
)

original_story = first_completion.choices[0].message.content
print("Historia original: \n", original_story)

summary_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "You are a summarization assistant."},
        {"role": "user",
         "content": f"I want you to summarize in 50-70 words the following story: {original_story}"}],
    temperature=temp,
)

first_summary = summary_completion.choices[0].message.content
print("Resumen: \n", summary_completion.choices[0].message.content)

first_reconstruction_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "user", "content": f"Imagine the original 150-180 word story from this summary: {first_summary}"}],
    temperature=temp,
)
first_reconstruction = first_reconstruction_completion.choices[0].message.content
print("Reconstrucción: \n", first_reconstruction)

second_summary_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "You are a summarization assistant."},
        {"role": "user",
         "content": f"I want you to summarize in 20-40 words the following story: {first_reconstruction}"}],
    temperature=temp,
)

second_summary = second_summary_completion.choices[0].message.content
print("Segundo resumen: \n", second_summary)

second_reconstruction_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "user", "content": f"Imagine the original 200-220 word story from this summary: {first_summary}"}],
    temperature=temp,
)
second_reconstruction = second_reconstruction_completion.choices[0].message.content
print("Segunda reconstrucción: \n", second_reconstruction)

cursor.execute(
    "INSERT INTO story_summary_reconstruction (model, temp, original_story, first_summary, first_reconstruction, "
    "second_summary, second_reconstruction) VALUES ("
    "%s, %s, %s, %s, %s, %s, %s)",
    (model, temp, original_story, first_summary, first_reconstruction, second_summary, second_reconstruction))
conexion.commit()
