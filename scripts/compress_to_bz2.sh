#!/bin/bash

# Lista de directorios a revisar
patch=("../left4dead2/models" "../left4dead2/sound")

# Lista de extensiones de archivos a comprimir
extensions=("*.mp3" "*.vtx" "*.mdl" "*.vvd")

for dir in "${patch[@]}"; do
    if [ -d "$dir" ]; then
        for ext in "${extensions[@]}"; do
            # Obtener todos los archivos con las extensiones especificadas en el directorio actual y subdirectorios
            find "$dir" -type f -name "$ext" | while read -r file; do
                bz2FileName="$file.bz2"
                
                # Verificar si el archivo .bz2 ya existe
                if [ ! -f "$bz2FileName" ]; then
                    # Comprimir el archivo en formato .bz2
                    echo "Comprimiendo $file a $bz2FileName"
                    brotli -o "$bz2FileName" "$file"
                else
                    echo "El archivo $bz2FileName ya existe. Saltando compresión."
                fi
            done
        done
    else
        echo "El directorio $dir no existe. Saltando."
    fi
done
