from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")

def get_text_embedding(text):
    embedding = model.encode(text).tolist()
    print(f"✅ Modelo cargado: {model}")  # Imprimir información del modelo
    print(f"✅ Embedding generado con {len(embedding)} dimensiones")
    return embedding
