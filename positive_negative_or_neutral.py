from openai import OpenAI
import mysql.connector

conexion = mysql.connector.connect(host="localhost", user="juan", password="mysqljuan", database="reviews")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM reviews")
registros = cursor.fetchall()

client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")

positives = {}
negatives = {}
neutral = {}

for registro in registros:
    messages = [
        {"role": "system", "content": "You are an expert at identifying whether a review for a speaker is positive, "
                                      "negative or neutral. I want you to include in your response the tag "
                                      "'positive' if the review is positive, 'negative' if the review is negative, "
                                      "and 'neutral' if the review is neutral. You can use just one tag."},
        {"role": "user", "content": registro[4]}
    ]
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages, temperature=1.0)
    response = completion.choices[0].message.content

    messages = [
        {"role": "system", "content": "You are an expert at estimating the number of stars a user would give in a "
                                      "review. Please estimate the number of stars for this review."},
        {"role": "user", "content": registro[4]}
    ]
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages, temperature=1.0)
    stars = completion.choices[0].message.content

    if "\'positive\'" in response:
        positives[registro[1]] = list(registro) + [response, stars]
        print("Positive:\n Name: ", registro[1], "\nReal stars: ", registro[2], "\nResponse: ", response, "\nStars: ", stars)
    elif "\'negative\'" in response:
        negatives[registro[1]] = list(registro) + [response, stars]
        print("Negative:\n ", registro[1], "\nReal stars: ", registro[2], "\nResponse: ", response, "\nStars: ", stars)
    elif "\'neutral\'" in response:
        neutral[registro[1]] = list(registro) + [response, stars]
        print("Neutral:\n ", registro[1], "\nReal stars: ", registro[2], "\nResponse: ", response, "\nStars: ", stars)

cursor.close()
conexion.close()

print("Positives: ")
for key, value in positives.items():
    print(key, value[2])
print("\nNegatives: ")
for key, value in negatives.items():
    print(key, value[2])
print("\nNeutral: ")
for key, value in neutral.items():
    print(key, value[2])
