from openai import OpenAI
import mysql.connector

model = "Rocket-3B"
temp = 1.0

conexion = mysql.connector.connect(host="localhost", user="juan", password="mysqljuan", database="llamafiles")
cursor = conexion.cursor()

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-no-key-required"
)
completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "I want you to invent a story about cats and dogs."
                                      "I want it to be between 100 and 200 words long."},
    ],
    temperature=temp,
)

original_story = completion.choices[0].message.content
print("Historia original: \n", original_story)

new_message = {"role": "user", "content": f"I want you to summarize the following story: {original_story}"}

messages = [
    {"role": "system", "content": "You are a summarization assistant."},
    new_message
]
temp = 0.0
summary_completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=messages,
    temperature=temp,
)

print("Resumen: \n", summary_completion.choices[0].message.content)

cursor.execute("INSERT INTO story_summary_reconstruction (model, original_story) VALUES (%s, %s)",
               (model, completion.choices[0].message.content))
conexion.commit()
