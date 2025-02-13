from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"
embedding_model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")

def search_files(query):
    """ Búsqueda optimizada para mejorar precisión y encontrar coincidencias exactas."""
    query = query.lower()
    query_vector = embedding_model.encode(query).tolist()
    
    search_query = {
        "size": 15,  # Aumentamos el número de resultados para mejorar precisión
        "query": {
            "bool": {
                "should": [
                    {  # 🔍 Coincidencia exacta en el contenido (prioridad más alta)
                        "match_phrase": {
                            "content": {
                                "query": query,
                                "boost": 5  # Aumentamos el peso para coincidencias exactas
                            }
                        }
                    },
                    {  # 🔍 Coincidencia exacta en el nombre del archivo
                        "match_phrase": {
                            "file_name": {
                                "query": query,
                                "boost": 3  # Más peso, pero menos que el contenido
                            }
                        }
                    },
                    {  # 🔍 Búsqueda semántica (vector embeddings), pero con MENOS peso
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 0.5",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    {  # 🔍 Búsqueda difusa con MENOS peso (para tolerancia de errores)
                        "match": {
                            "content": {
                                "query": query,
                                "fuzziness": "1",  # 🔥 Permitimos solo 1 error en la palabra
                                "boost": 1.5
                            }
                        }
                    },
                    {  # 🔍 Coincidencias parciales en contenido (prefijo)
                        "match_phrase_prefix": {
                            "content": {
                                "query": query,
                                "boost": 2  # Más peso para encontrar términos parciales
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    }

    response = es.search(index=index_name, body=search_query)
    
    results = [
        {
            "name": hit["_source"]["file_name"],
            "path": hit["_source"]["file_path"],
            "size": hit["_source"].get("file_size", "Desconocido"),
            "modified_time": hit["_source"].get("modified_time", "Desconocida"),
            "score": hit["_score"],
            "preview": hit["_source"]["content"][:300] if "content" in hit["_source"] else "No se pudo extraer contenido"
        }
        for hit in response["hits"]["hits"]
    ]

    return results
