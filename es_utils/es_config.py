from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"

def create_index():
    """Crea el índice en Elasticsearch si no existe."""
    if not es.indices.exists(index=index_name):
        mappings = {
            "mappings": {
                "properties": {
                    "file_name": {"type": "text"},  # 📌 Permite búsquedas por nombre
                    "file_extension": {"type": "keyword"},  # 📌 Filtrar por tipo de archivo
                    "file_path": {"type": "text"},
                    "content": {"type": "text"},  # 📌 Búsqueda de texto completo en contenido
                    "vector": {"type": "dense_vector", "dims": 768}  # 📌 Búsqueda semántica
                }
            }
        }
        es.indices.create(index=index_name, body=mappings)
        print(f"✅ Índice '{index_name}' creado correctamente.")
    else:
        print(f"⚠️ Índice '{index_name}' ya existe.")
