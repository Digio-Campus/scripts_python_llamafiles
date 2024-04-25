from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from llama_index.embeddings.llamafile import LlamafileEmbedding
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
import asyncio

url = ('mongodb+srv://94juanvalera94:mongodbjuan@cluster0.sd2zhrd.mongodb.net/?retryWrites=true&w=majority&appName'
       '=Cluster0')
client = MongoClient(url)
db = client['penguin']

openai = OpenAI(base_url="http://127.0.0.1:8081/v1", api_key="sk-no-key-required")

story = ("Once upon a time in the quirky town of Whimsyville, there was a particularly peculiar penguin named Percy. "
         "Unlike his fellow flightless friends, Percy had an insatiable desire to soar through the sky like a "
         "majestic eagle. So, armed with a pair of homemade wings fashioned from discarded banana peels and rubber "
         "bands, Percy embarked on his daring quest to defy gravity.")

collection = db['chunk_size_250_overlap_70']
splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=70)

embedding = LlamafileEmbedding(
    base_url="http://localhost:8080"
)


# embeddings = OpenAIEmbeddings(api_key="empty", configuration={"baseURL": "http://localhost:8080/v1"})


# Función para la inserción de datos en la base de datos
async def insert_data(collection, embedding, splitter, documents_to_insert):
    doc_output_to_insert = splitter.split_documents(documents_to_insert)
    page_contents = [document.page_content for document in doc_output_to_insert]
    vectors = embedding.get_text_embedding_batch(page_contents, show_progress=True, timeout=160)
    insert_many_result = collection.insert_many([
        {"id": index, "document": doc_output_to_insert[index], "vector": vector}
        for index, vector in enumerate(vectors)
    ])
    print(insert_many_result)


# Función para la búsqueda vectorial y la interacción con el modelo de OpenAI
async def vector_search_and_model_interaction(collection, embedding, query, openai):
    vector_query = embedding.get_text_embedding_batch([query])
    print(vector_query)
    agg = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "vector",
                "queryVector": vector_query[0],
                "numCandidates": 100,
                "limit": 5
            }
        },
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "document.pageContent": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    aggregate_result = collection.aggregate(agg)
    async for doc in aggregate_result:
        print(doc)
    completion = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": f"This is the context to look for information {aggregate_result}"},
            {"role": "user", "content": query}
        ],
        model="LLaMA_CPP"
    )
    print(completion.choices[0])


documents_to_insert = [Document(page_content=story)]


# Wrap the await calls inside an async function
async def main():
    await insert_data(collection, embedding, splitter, documents_to_insert)
    await vector_search_and_model_interaction(collection, embedding, "What was Percy's desire?", openai)
    await client.close()


# Run the main function using an event loop

asyncio.run(main())
