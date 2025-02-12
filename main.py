from es_utils import search_files

def main():
    print("\n📂 Motor de Búsqueda Híbrido (Texto, Imágenes, Videos)")
    
    while True:
        query = input("🔍 Ingresa tu consulta de búsqueda (o 'salir' para terminar): ")
        if query.lower() == "salir":
            break

        file_type = input("📌 Filtrar por tipo de archivo (ejemplo: pdf, txt, docx) o presiona Enter: ")

        results = search_files(query, file_type if file_type else None)

        if results:
            print("\n🔎 Resultados de búsqueda:")
            for name, path, score in results:
                print(f"📌 {name} - {path} (Score: {score:.2f})")
        else:
            print("⚠️ No se encontraron coincidencias.")

if __name__ == "__main__":
    main()
