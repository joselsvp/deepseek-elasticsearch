from elasticsearch import Elasticsearch
from models.text_model import get_text_embedding

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"

def search_files(query, file_type=None):
    """Búsqueda híbrida: combina búsqueda semántica y búsqueda tradicional."""

    query_vector = get_text_embedding(query)  # Genera el embedding del texto

    search_query = {
        "size": 10,
        "query": {
            "bool": {
                "should": [
                    {  # 🔍 Búsqueda semántica con similitud coseno
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    {  # 🔍 Búsqueda por contenido de texto
                        "match": {"content": query}
                    },
                    {  # 🔍 Búsqueda por nombre de archivo
                        "match": {"file_name": query}
                    }
                ],
                "minimum_should_match": 1
            }
        }
    }

    # 📌 Filtrar por tipo de archivo si el usuario lo especifica
    if file_type:
        search_query["query"]["bool"]["filter"] = [
            {"term": {"file_extension": file_type}}
        ]

    # 🔍 Ejecutar búsqueda en Elasticsearch
    response = es.search(index=index_name, body=search_query)

    results = [(hit["_source"]["file_name"], hit["_source"]["file_path"], hit["_score"]) for hit in response["hits"]["hits"]]

    return results
