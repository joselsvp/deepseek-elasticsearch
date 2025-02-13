import datetime
import os
import time
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from utils.extract_text import extract_text

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"
embedding_model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")  # 🔥 Modelo de embeddings

def index_files(folder_path):
    """ Recorre una carpeta y almacena archivos en Elasticsearch con embeddings. """
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            # Extraer contenido de cualquier archivo posible
            content = extract_text(file_path)
            if content is None:
                print(f"⚠️ No se pudo extraer contenido de: {file_path}")
                continue  # Saltar archivos sin contenido

            # Generar vector semántico 🔥
            vector = embedding_model.encode(content.lower()).tolist()

            # Obtener metadatos del archivo
            file_size = os.path.getsize(file_path)
            modified_time = time.ctime(os.path.getmtime(file_path))
            # 🔥 Convertir `modified_time` a formato ISO-8601
            modified_timestamp = os.path.getmtime(file_path)
            modified_time = datetime.datetime.utcfromtimestamp(modified_timestamp).isoformat() + "Z"

            doc = {
                "file_name": file.lower(),
                "file_path": file_path,
                "file_size": file_size,
                "modified_time": modified_time,
                "content": content.lower(),
                "vector": vector  # 🚀 Embedding para búsqueda semántica
            }

            es.index(index=index_name, body=doc)
            print(f"✅ Archivo indexado: {file}")

# Ejecutar la indexación
index_files("data/")
