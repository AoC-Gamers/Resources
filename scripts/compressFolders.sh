#!/bin/bash

# Carpetas a comprimir
folders_to_compress=(
    "../left4dead2/"
)

# Comprimir cada carpeta
for folder in "${folders_to_compress[@]}"; do
    if [ -d "$folder" ]; then
        folder_name=$(basename "$folder")
        zip -r "${folder_name}.zip" "$folder"
        echo "Carpeta $folder comprimida en ${folder_name}.zip"
    else
        echo "Carpeta $folder no encontrada"
    fi
done
