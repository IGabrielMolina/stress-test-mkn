import os

# Qué buscar y por qué reemplazarlo (Cambiá 'mkn' por 'nexus' si preferís)
OLD_WORD = "mkn"
NEW_WORD = "mkn"

# Solo tocamos código, ignoramos imágenes y bases de datos
ALLOWED_EXTENSIONS = {'.py', '.yml', '.yaml', '.md', '.json', '.env', '.sh', '.txt'}
EXCLUDE_DIRS = {'.git', 'venv', '__pycache__', 'data', 'node_modules', 'postgres_data', 'redis_data'}

def replace_in_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Ignorar carpetas peligrosas
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificamos si la palabra existe (sin importar mayúsculas)
                    if OLD_WORD.lower() in content.lower():
                        # Reemplazamos manteniendo el formato original (minúscula, Mayúscula inicial, TODO MAYÚSCULA)
                        content = content.replace(OLD_WORD.lower(), NEW_WORD.lower())
                        content = content.replace(OLD_WORD.capitalize(), NEW_WORD.capitalize())
                        content = content.replace(OLD_WORD.upper(), NEW_WORD.upper())
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Modificado limpio: {filepath}")
                except Exception as e:
                    print(f"⚠️ No se pudo leer {filepath}: {e}")

if __name__ == "__main__":
    print("Iniciando limpieza de nombre...")
    replace_in_files('.')
    print("¡Limpieza terminada!")
