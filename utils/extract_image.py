from models.clip_model import get_image_embedding

def extract_image_embedding(image_path):
    """Extrae embeddings de una imagen y maneja errores."""
    vector = get_image_embedding(image_path)
    
    if vector is None:
        raise ValueError(f"❌ No se pudo procesar la imagen {image_path}")
    
    return vector
