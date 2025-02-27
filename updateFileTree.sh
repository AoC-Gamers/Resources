#!/bin/bash

# Instalar dependencias
npm install

# Generar el árbol de archivos
npm run generate

echo "El árbol de archivos ha sido actualizado y guardado en file-tree.json"
