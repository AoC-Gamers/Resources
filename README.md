# AoC Gamers Resources

Este proyecto publica recursos estaticos para usuarios y servidores de AoC Gamers. Incluye paginas HTML simples, recursos multimedia, archivos comprimidos y un indice navegable del arbol de archivos.

## Requisitos

- Node.js 22 o superior.
- npm, incluido con Node.js.

No se requiere Ruby, Jekyll, MSYS2 ni DevKit para compilar el proyecto.

## Contenido del Proyecto

### Servermessage

Paginas HTML estaticas usadas por servidores u otros servicios. Las paginas se generan desde la configuracion:

```text
src/config/servermessage-pages.json
```

El build escribe los HTML finales en:

```text
servermessage/
```

Las paginas pueden definir imagenes alternativas en `images`. Si una pagina tiene alternativas, se puede seleccionar una imagen por URL:

```text
/servermessage/motd.html?img=classic02
```

```text
/servermessage/host.html?img=host
```

`host.html` solo permite imagenes dentro de `/servermessage/img/host/`.

Tambien se puede usar una ruta directa permitida por la configuracion:

```text
/servermessage/motd.html?src=/servermessage/img/motd/patas04.png
```

Las imagenes usadas por esas paginas se guardan en:

```text
servermessage/img/
```

Para nuevas imagenes que no pertenezcan a una categoria existente, usa:

```text
servermessage/img/custom/
```

### Left4Dead2

Recursos como archivos MDR, MP3, BZ2, etc., necesarios para los clientes de los servidores de juego.

El build comprime la carpeta:

```text
left4dead2/
```

y genera:

```text
left4dead2.zip
```

### Arbol de Archivos

`index.html` actua como indice principal del proyecto. Lee los archivos generados en `filetree/` para mostrar el arbol de archivos y las carpetas comprimidas disponibles.

El indice incluye busqueda por nombre, filtro por extension, tamano de archivo, hash SHA-256 corto y botones para copiar URLs directas.

El build genera:

- `filetree/file-tree.json`
- `filetree/compressed-files.json`
- `filetree/manifest.json`
- `filetree/redirects.json`
- `.nojekyll`

`.nojekyll` indica a GitHub Pages que publique el contenido como archivos estaticos, sin procesarlo con Jekyll.

`manifest.json` incluye tamano y hash SHA-256 de cada archivo publico generado o servido.

## Uso

Instala dependencias:

```bash
npm install
```

Compila todo el proyecto:

```bash
npm run build
```

Tambien puedes usar los wrappers por sistema:

```bash
./build.sh
```

```powershell
.\build.ps1
```

Los tres comandos ejecutan el mismo build Node:

```bash
node ./scripts/build.js
```

## Publicacion en GitHub Pages

El proyecto queda listo para publicarse como sitio estatico desde GitHub Pages. Configura Pages para publicar desde la rama correspondiente y la raiz del repositorio.

Como el repo incluye `.nojekyll`, GitHub Pages no necesita compilar Jekyll. Los archivos generados se sirven directamente.

## Integracion Continua

El workflow de GitHub Actions en `.github/workflows/build.yml` usa Node.js 22, ejecuta `npm ci`, corre `npm run build` y verifica que los archivos generados esten actualizados con `git diff --exit-code`.

## Scripts Principales

- `src/build/build.js`: build principal en Node.
- `src/build/exclusions.js`: define archivos y directorios excluidos del arbol, manifiesto y redirects.
- `src/config/servermessage-pages.json`: define las paginas HTML generadas para `servermessage`.
- `scripts/build.js`: wrapper estable para ejecutar el build desde npm, Bash y PowerShell.
- `build.sh`: wrapper Bash compatible.
- `build.ps1`: wrapper PowerShell compatible.
- `.nvmrc` y `.node-version`: fijan Node.js 22 para gestores de version.

## Notas

- Los archivos dentro de `filetree/` y `left4dead2.zip` se regeneran con `npm run build`.
- Si agregas una nueva pagina `servermessage`, anadela primero a `src/config/servermessage-pages.json`.
- El build valida que cada imagen declarada en `src/config/servermessage-pages.json` exista.
- Si agregas archivos internos que no deben aparecer en el indice publico, agregalos a `src/build/exclusions.js`.
