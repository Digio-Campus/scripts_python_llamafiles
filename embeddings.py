from llama_index.embeddings.llamafile import LlamafileEmbedding

embedding = LlamafileEmbedding(
    base_url="http://localhost:8080",
)

pass_embedding = embedding.get_text_embedding_batch(
    ["This is a passage!", "This is another passage"], show_progress=True
)
print(len(pass_embedding), len(pass_embedding[0]))

query_embedding = embedding.get_query_embedding("Where is blue?")
print(len(query_embedding))
print(query_embedding[:10])
