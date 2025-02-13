from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

es = Elasticsearch("http://localhost:9200/")
index_name = "multimedia"
embedding_model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")

def search_files(query):
    """ Búsqueda híbrida optimizada: semántica + texto exacto + autocompletado."""
    
    query = query.lower()
    query_vector = embedding_model.encode(query).tolist()
    
    search_query = {
        "size": 15,  # Aumentamos la cantidad de resultados para mejorar precisión
        "query": {
            "bool": {
                "should": [
                    {  # 🔍 Coincidencia exacta en el contenido
                        "match_phrase": {
                            "content": {
                                "query": query,
                                "boost": 3
                            }
                        }
                    },
                    {  # 🔍 Coincidencia exacta en el nombre del archivo
                        "match_phrase": {
                            "file_name": {
                                "query": query,
                                "boost": 2.5
                            }
                        }
                    },
                    {  # 🔍 Búsqueda por embeddings
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    {  # 🔍 Búsqueda difusa con mayor tolerancia a errores
                        "match": {
                            "content": {
                                "query": query,
                                "fuzziness": "AUTO",  # 🔥 Permite más errores tipográficos
                                "boost": 1.2
                            }
                        }
                    },
                    {  # 🔍 Autocompletado en nombres de archivos
                        "match_phrase_prefix": {
                            "file_name": {
                                "query": query,
                                "boost": 1.5
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
