#!/bin/bash
set -e

if command -v node >/dev/null 2>&1; then
  node ./scripts/build.js
elif command -v node.exe >/dev/null 2>&1; then
  node.exe ./scripts/build.js
elif command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./build.ps1
else
  echo "Node.js no esta disponible en PATH. Instala Node.js o ejecuta .\\build.ps1 desde PowerShell." >&2
  exit 1
fi
