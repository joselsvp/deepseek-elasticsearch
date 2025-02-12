import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# Cargar modelo CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_image_embedding(image_path):
    """Genera un embedding para una imagen con CLIP."""
    try:
        # Cargar imagen
        image = Image.open(image_path).convert("RGB")
        
        # Preprocesar imagen para CLIP
        inputs = processor(images=image, return_tensors="pt")
        
        # Generar embeddings
        with torch.no_grad():
            vector = model.get_image_features(**inputs)  # Obtener embedding de la imagen
        
        return vector.squeeze().tolist()  # Convertir a lista de Python
    except Exception as e:
        print(f"❌ Error generando embedding de imagen {image_path}: {e}")
        return None
