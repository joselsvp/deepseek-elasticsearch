from elasticsearch import Elasticsearch  # Importar desde la librería oficial

from .es_config import create_index
from .es_index import index_files
from .es_search import search_files

# Crear conexión global a Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    verify_certs=False,  # Desactiva verificación SSL
    ssl_show_warn=False  # Oculta advertencias de SSL
)
# Definir el índice globalmente
index_name = "multimedia"
