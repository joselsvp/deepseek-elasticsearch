from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"

def create_index():
    """ Crea un índice en Elasticsearch con análisis en minúsculas. """
    settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_lowercase_analyzer": {  # Analizador que convierte texto a minúsculas
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "file_name": {
                    "type": "text",
                    "analyzer": "custom_lowercase_analyzer"  # Aplica minúsculas al indexar
                },
                "content": {
                    "type": "text",
                    "analyzer": "custom_lowercase_analyzer"  # Aplica minúsculas al contenido
                },
                "file_path": {"type": "keyword"},
                "file_size": {"type": "long"},
                "modified_time": {"type": "date"}
            }
        }
    }

    es.indices.create(index=index_name, body=settings, ignore=400)
    print(f"✅ Índice '{index_name}' creado con análisis en minúsculas.")

# Ejecutar al inicio para configurar el índice correctamente
create_index()
