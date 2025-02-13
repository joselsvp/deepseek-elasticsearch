import datetime
import os
import time
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from utils.extract_text import extract_text

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"
embedding_model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")

def file_already_indexed(file_name, modified_time):
    """ Verifica si un archivo ya está indexado y si ha sido modificado."""
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"file_name": file_name}},
                    {"match": {"modified_time": modified_time}}
                ]
            }
        }
    }
    response = es.search(index=index_name, body=query)
    return len(response["hits"]["hits"]) > 0

def index_files(folder_path):
    """ Recorre una carpeta y almacena archivos en Elasticsearch con embeddings, evitando duplicados."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            # Extraer contenido de cualquier archivo posible
            extracted_data = extract_text(file_path)
            if not extracted_data or not extracted_data.get("full_text"):
                print(f"⚠️ Archivo sin contenido válido: {file_path}, saltando...")
                continue  # Saltar archivos sin contenido
            
            content = extracted_data["full_text"]
            summary = extracted_data.get("summary", "")
            sections = extracted_data.get("sections", [])
            
            # Verificar si content es válido antes de generar embeddings
            if content:
                vector = embedding_model.encode(content.lower()).tolist()
            else:
                print(f"⚠️ No se pudo generar embeddings para: {file_path}, saltando...")
                continue

            # Obtener metadatos del archivo
            file_size = os.path.getsize(file_path)
            modified_timestamp = os.path.getmtime(file_path)
            modified_time = datetime.datetime.utcfromtimestamp(modified_timestamp).isoformat() + "Z"

            # Verificar si el archivo ya está indexado y actualizado
            if file_already_indexed(file.lower(), modified_time):
                print(f"🔄 Archivo ya indexado sin cambios: {file}")
                continue

            doc = {
                "file_name": file.lower(),
                "file_path": file_path,
                "file_size": file_size,
                "modified_time": modified_time,
                "content": content.lower(),
                "summary": summary.lower(),
                "sections": sections,
                "vector": vector  # 🚀 Embedding para búsqueda semántica
            }

            es.index(index=index_name, body=doc)
            print(f"✅ Archivo indexado: {file}")

# Ejecutar la indexación evitando duplicados
index_files("data/")
