# AoC Gamers Resources

Este proyecto proporciona recursos para usuarios y servidores, facilitando la gestión de páginas estáticas, recursos multimedia y archivos de redirección para diferentes servicios y juegos.

## Contenido del Proyecto

### Servermessage

- **Descripción:**  
  Páginas estáticas creadas con Jekyll en Ruby. Los archivos HTML se generan a partir de una plantilla base en `_layouts/default.html`. También se guardan imágenes usadas en servidores u otros servicios (logos, mensajes del día, etc.).

- **Requisitos:**  
  Ruby y MSYS2/DevKit (o herramientas de desarrollo correspondientes) para compilar dependencias y ejecutar Jekyll.

- **Desarrollo y Uso:**  
  - Para compilar dependencias o realizar cambios en los archivos HTML, ejecuta:
    ```bash
    bundle install
    ```
  - Para iniciar el servidor local y probar el sitio, usa:
    ```bash
    bundle exec jekyll serve
    ```
    El sitio estará disponible en [http://127.0.0.1:4000](http://127.0.0.1:4000).

### Left4Dead2

- **Descripción:**  
  Recursos como archivos MDR, MP3, etc., necesarios para los clientes de los servidores de juego.

- **Actualización de Recursos:**  
  Actualiza la tabla de descargas del complemento que utiliza algún recurso y sube el archivo correspondiente al directorio adecuado.

- **Script de Compresión:**  
  Incluye un script que comprime la carpeta en un archivo `.zip`, facilitando la descarga manual al cliente.

### Árbol de Archivos

- **Descripción:**  
  `index.html` actúa como índice principal del proyecto, mostrando recursivamente el árbol de archivos generado a partir de `file-tree.json`.

- **Generación del Árbol:**  
  Ejecuta el script `build.sh`, que invoca los siguientes scripts secundarios:
  
  - **exclusions.js:**  
    Define archivos y directorios a excluir en otros scripts.
  
  - **generateFileTree.js:**  
    Genera un árbol de archivos en formato JSON, excluyendo elementos definidos en `exclusions.js`. El resultado se guarda en `file-tree.json` y también se genera una lista de archivos comprimidos en `compressed-files.json`.
  
  - **generateRedirects.js:**  
    Genera un archivo de redirecciones (`redirects.json`) para el sitio web estático, excluyendo elementos definidos en `exclusions.js`. Cada archivo se redirige a `index.html`.
  
  - **compressFolders.sh:**  
    Comprime las carpetas especificadas en archivos `.zip`. Las carpetas a comprimir se definen dentro del script.

## Uso y Ejecución

1. **Instalación de Dependencias:**  
   Asegúrate de tener instalado Ruby y MSYS2/DevKit. Luego, desde la raíz del proyecto, ejecuta:
   ```bash
   bundle install
   ```
2. **Compilación del Sitio (Servermessage):**  
   Para compilar y ver los cambios en las páginas estáticas, inicia el servidor local con:
   ```bash
   bundle exec jekyll serve
   ```
   Visita [http://127.0.0.1:4000](http://127.0.0.1:4000) para ver el sitio en acción.
3. **Generar Árbol y Redirecciones:**  
   Ejecuta el script de construcción:
   ```bash
   ./build.sh
   ```
   Esto generará:
  - El árbol de archivos (`file-tree.json`).
  - La lista de archivos comprimidos (`compressed-files.json`).
  - El archivo de redirecciones (`_redirects`).
  - Además, comprimirá las carpetas especificadas.

## Notas Adicionales
1. **GitHub Pages y Jekyll:**  
   El proyecto se puede desplegar en GitHub Pages. Se recomienda ignorar en Git los archivos generados, por ejemplo, `_site/`, agregándolos a `.gitignore`.

2. **Optimización de Scripts:**  
   Los scripts `generateFileTree.js` y `generateRedirects.js` utilizan `exclusions.js` para definir archivos y directorios a excluir, asegurando una única fuente de verdad y facilitando el mantenimiento.