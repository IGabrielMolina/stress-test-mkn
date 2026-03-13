import os

WORD_TO_FIND = "makini"

# Carpetas a ignorar para no buscar en la base de datos ni en git
EXCLUDE_DIRS = {'.git', 'venv', '__pycache__', 'data', 'node_modules', 'postgres_data', 'redis_data'}
# Solo buscamos en archivos de texto legibles
ALLOWED_EXTENSIONS = {'.py', '.yml', '.yaml', '.md', '.json', '.env', '.sh', '.txt'}

def check_files(root_dir):
    found_something = False
    print(f"🔍 Escaneando el proyecto en busca de '{WORD_TO_FIND}'...\n")
    
    for root, dirs, files in os.walk(root_dir):
        # Ignorar las carpetas prohibidas
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line_number, line in enumerate(lines, 1):
                            # Buscamos sin importar mayúsculas o minúsculas
                            if WORD_TO_FIND.lower() in line.lower():
                                print(f"🚨 ALERTA en -> {filepath} (Línea {line_number})")
                                print(f"   Texto exacto: {line.strip()}\n")
                                found_something = True
                except Exception:
                    pass # Ignoramos archivos que den error de lectura
    
    if not found_something:
        print("✅ ¡ESPECTACULAR! Todo limpio. No quedó ni un solo rastro en el código.")

if __name__ == "__main__":
    check_files('.')
