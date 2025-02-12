import os
from elasticsearch import Elasticsearch
from utils.extract_text import extract_text
from models.text_model import get_text_embedding

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"

def index_files(folder_path):
    """ Recorre una carpeta y almacena archivos en Elasticsearch. """
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            content = extract_text(file_path) if ext.lower() in [".txt", ".pdf", ".docx"] else None
            vector = get_text_embedding(content) if content else None

            doc = {
                "file_name": file,
                "file_extension": ext.lower().replace(".", ""),
                "file_path": file_path,
                "content": content,
                "vector": vector
            }

            es.index(index=index_name, body=doc)
            print(f"📂 Archivo indexado: {file}")

# Ejecutar la indexación
index_files("data/")
