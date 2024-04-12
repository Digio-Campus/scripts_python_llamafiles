from openai import OpenAI
import mysql.connector

model = "Phi-temp 0"


def get_review_messages(content, registro):
    return [
        {"role": "system", "content": content},
        {"role": "user", "content": registro[3]}
    ]


def get_insert_query_speaker_product_reviews(field):
    return f"""
        INSERT INTO speaker_product_reviews (id, {field})
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        {field} = VALUES({field})
    """


def get_insert_query_general_results(field):
    return f"""
        INSERT INTO general_results (modelo, {field})
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        {field} = VALUES({field})
    """


def process_review(field, client, messages, cursor, conexion, registro):
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages, temperature=0.0, max_tokens=100)
    response = "\n" + completion.choices[0].message.content
    cursor.execute(get_insert_query_speaker_product_reviews(field), (registro[0], response))
    conexion.commit()
    return response


def process_global_review(field, client, messages, cursor, conexion, registro):
    completion = client.chat.completions.create(model="LLaMA_CPP", messages=messages, temperature=0.0, max_tokens=100)
    response = "\n" + completion.choices[0].message.content
    cursor.execute(get_insert_query_general_results(field), (model, response))
    conexion.commit()
    print("\nGlobal design response field: ", field, response)


def main():
    conexion = mysql.connector.connect(host="localhost", user="juan", password="mysqljuan", database="reviews")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM speaker_product_reviews")
    registros = cursor.fetchall()

    client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="sk-no-key-required")

    for registro in registros:
        design_messages = get_review_messages(
            "Please provide in just one sentence the essence of what the user thinks about the physical design of the "
            "product. Please focus just on the physical design and don't invent anything that is not in the review"
            " nor focus on other aspects of the product. ",
            registro)
        design_response = process_review('design', client, design_messages, cursor, conexion, registro)

        shipping_messages = get_review_messages(
            "Please provide in just one sentence the essence of what the user thinks about the shipping of the "
            "product. Please focus just on the shipping and don't invent anything that is not in the review"
            " nor focus on other aspects of the product. ",
            registro)
        shipping_response = process_review('shipping', client, shipping_messages, cursor, conexion, registro)

        price_messages = get_review_messages(
            "Please provide in just one sentence the essence of what the user thinks about the pricing of the "
            "product. Please focus just on the pricing and don't invent anything that is not in the review nor focus"
            "on other aspects of the product. ",
            registro)
        price_response = process_review('price', client, price_messages, cursor, conexion, registro)

        maxVolume_messages = get_review_messages(
            "Please provide in just one sentence the essence of what the user thinks about the feature"
            " maxVolume of the product. Please focus just on the feature maxVoume and don't invent anything"
            " that is not in the review nor focus on other aspects of the product. ",
            registro)
        maxVolume_response = process_review('maxVolume', client, maxVolume_messages, cursor, conexion, registro)

        print("\nReview from: ", registro[1], "\nStars: ", registro[2], "\nReview: ", registro[3],
              "\nDesign response: ", design_response, "\nShipping response: ", shipping_response,
              "\nPrice response: ", price_response, "\nMaxVolume response: ", maxVolume_response)

    all_design_reviews = "\n".join(registro[4] for registro in registros)
    print("\nAll design reviews: ", all_design_reviews)

    design_messages = get_review_messages(
        "I want you to provide a global assessment of what customers think about the physical design of the product."
        "The product is a new speaker and the company wants to know what their customers think about it."
        " You are going to receive some responses from an AI model summarizing customer's reviews. "
        "Write a summary with the main points. Include the most common positive and negative aspects of the design.",
        all_design_reviews)
    process_global_review('design', client, design_messages, cursor, conexion, registros[0])

    all_shipping_reviews = "\n".join(registro[5] for registro in registros)
    print("\nAll shipping reviews: ", all_shipping_reviews)

    shipping_messages = get_review_messages(
        "I want you to provide a global assessment of what customers think about the shipping of the product."
        "The product is a new speaker and the company wants to know what their customers think about it."
        " You are going to receive some responses from an AI model summarizing customer's reviews. "
        "Write a summary with the main points. Include the most common positive and negative aspects of the shipping.",
        all_shipping_reviews)
    process_global_review('shipping', client, shipping_messages, cursor, conexion, registros[0])

    all_price_reviews = "\n".join(registro[6] for registro in registros)
    print("\nAll price reviews: ", all_price_reviews)

    price_messages = get_review_messages(
        "I want you to provide a global assessment of what customers think about the price of the product."
        "The product is a new speaker and the company wants to know what their customers think about it."
        " You are going to receive some responses from an AI model summarizing customer's reviews. "
        "Write a summary with the main points. Include the most common positive and negative aspects of the price.",
        all_price_reviews)
    process_global_review('price', client, price_messages, cursor, conexion, registros[0])

    all_maxVolume_reviews = "\n".join(registro[7] for registro in registros)
    print("\nAll maxVolume reviews: ", all_maxVolume_reviews)

    maxVolume_messages = get_review_messages(
        "I want you to provide a global assessment of what customers think about the maxVolume of the product."
        "The product is a new speaker and the company wants to know what their customers think about it."
        " You are going to receive some responses from an AI model summarizing customer's reviews. "
        "Write a summary with the main points. Include the most common positive and negative aspects of the maxVolume.",
        all_maxVolume_reviews)
    process_global_review('maxVolume', client, maxVolume_messages, cursor, conexion, registros[0])

    cursor.close()
    conexion.close()


if __name__ == "__main__":
    main()
