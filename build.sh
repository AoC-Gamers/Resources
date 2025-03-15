#!/bin/bash

# Ejecutar el script de compresión de carpetas
./scripts/compressFolders.sh

# Ejecutar el script de generación del árbol de archivos
node ./scripts/generateFileTree.js

# Ejecutar el script de generación de redirecciones
node ./scripts/generateRedirects.js

echo "Build completado correctamente."
