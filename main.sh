#!/bin/bash

# Generar el árbol de archivos
node generateFileTree.js

# Generar el archivo de redirecciones
node generateRedirects.js

# Comprimir carpetas específicas
./compressFolders.sh

echo "El árbol de archivos ha sido actualizado y las carpetas especificadas han sido comprimidas."
