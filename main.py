from es_utils import search_files

def main():
    print("\n📂 Motor de Búsqueda con Lenguaje Natural (IA)")

    while True:
        query = input("🔍 Ingresa tu consulta de búsqueda (o 'salir' para terminar): ")
        if query.lower() == "salir":
            break

        results = search_files(query)

        if results:
            print("\n🔎 Resultados de búsqueda:")
            for result in results:
                print(f"\n📌 {result['name']} - {result['path']} (Tamaño: {result['size']} bytes, Modificado: {result['modified_time']}, Score: {result['score']:.2f})")
                print(f"📝 Fragmento: {result['preview']}")
        else:
            print("⚠️ No se encontraron coincidencias.")

if __name__ == "__main__":
    main()
