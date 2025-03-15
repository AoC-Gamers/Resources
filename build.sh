#!/bin/bash

# Generar el árbol de archivos
npm run generate

# Comprimir carpetas específicas
./compressFolders.sh

echo "El árbol de archivos ha sido actualizado y las carpetas especificadas han sido comprimidas."
