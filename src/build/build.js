const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const exclusions = require('./exclusions');
const serverMessagePages = require('../config/servermessage-pages.json');

const rootDir = path.resolve(__dirname, '..', '..');
const filetreeDir = path.join(rootDir, 'filetree');
const deterministicZipDate = new Date('2000-01-01T00:00:00Z');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function toPosixPath(value) {
  return value.split(path.sep).join('/');
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function validateImagePath(src, pageFile) {
  const imagePath = path.join(rootDir, src.replace(/^\//, ''));
  if (!fs.existsSync(imagePath)) {
    throw new Error(`Imagen no encontrada para ${pageFile}: ${src}`);
  }
}

function normalizePageImages(page) {
  const images = { default: page.src, ...(page.images || {}) };

  for (const [key, src] of Object.entries(images)) {
    if (!key || !src) {
      throw new Error(`Imagen invalida en ${page.file}.`);
    }

    validateImagePath(src, page.file);
  }

  return images;
}

function renderDynamicImageScript(images) {
  const imageEntries = JSON.stringify(images, null, 6);

  return `    <script>
      const allowedImages = ${imageEntries};
      const params = new URLSearchParams(window.location.search);
      const requestedImage = params.get('img');
      const requestedSource = params.get('src');
      const image = document.getElementById('servermessage-image');
      const allowedSources = new Set(Object.values(allowedImages));

      if (requestedImage && allowedImages[requestedImage]) {
        image.src = allowedImages[requestedImage];
      } else if (requestedSource && allowedSources.has(requestedSource)) {
        image.src = requestedSource;
      }
    </script>
`;
}

function renderServerMessages() {
  const outputDir = path.join(rootDir, 'servermessage');
  ensureDir(outputDir);

  for (const page of serverMessagePages) {
    if (!page.file || !page.title || !page.src) {
      throw new Error('Cada pagina servermessage debe definir file, title y src.');
    }

    const images = normalizePageImages(page);
    const dynamicImageScript = page.images ? renderDynamicImageScript(images) : '';

    const html = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>${escapeHtml(page.title)} AoC</title>
  </head>
  <body style="margin:0; padding:0; background:#000; overflow-y: hidden;">
    <img id="servermessage-image" alt="${escapeHtml(page.title)}" src="${escapeHtml(page.src)}" style="width:100%;height:100%;">
${dynamicImageScript}
  </body>
</html>
`;

    fs.writeFileSync(path.join(outputDir, page.file), html);
  }

  console.log('Paginas servermessage generadas correctamente.');
}

function createCrc32Table() {
  const table = new Uint32Array(256);

  for (let i = 0; i < 256; i += 1) {
    let value = i;
    for (let bit = 0; bit < 8; bit += 1) {
      value = value & 1 ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
    }
    table[i] = value >>> 0;
  }

  return table;
}

const crc32Table = createCrc32Table();

function crc32(buffer) {
  let value = 0xffffffff;

  for (const byte of buffer) {
    value = crc32Table[(value ^ byte) & 0xff] ^ (value >>> 8);
  }

  return (value ^ 0xffffffff) >>> 0;
}

function dosDateTime(date) {
  const year = Math.max(date.getUTCFullYear(), 1980);
  const dosTime =
    (date.getUTCHours() << 11) |
    (date.getUTCMinutes() << 5) |
    Math.floor(date.getUTCSeconds() / 2);
  const dosDate =
    ((year - 1980) << 9) |
    ((date.getUTCMonth() + 1) << 5) |
    date.getUTCDate();

  return { dosDate, dosTime };
}

function uint16(value) {
  const buffer = Buffer.alloc(2);
  buffer.writeUInt16LE(value);
  return buffer;
}

function uint32(value) {
  const buffer = Buffer.alloc(4);
  buffer.writeUInt32LE(value >>> 0);
  return buffer;
}

function collectFiles(dir, baseDir = dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      files.push(...collectFiles(fullPath, baseDir));
      continue;
    }

    if (entry.isFile()) {
      files.push({
        fullPath,
        zipPath: toPosixPath(path.relative(baseDir, fullPath)),
        stat: fs.statSync(fullPath)
      });
    }
  }

  return files;
}

function createStoredZip(sourceDir, outputFile) {
  if (!fs.existsSync(sourceDir)) {
    console.warn(`Carpeta ${path.relative(rootDir, sourceDir)} no encontrada.`);
    return;
  }

  const sourceName = path.basename(sourceDir);
  const files = collectFiles(sourceDir);
  const localParts = [];
  const centralParts = [];
  let offset = 0;

  for (const file of files) {
    const data = fs.readFileSync(file.fullPath);
    const name = Buffer.from(`${sourceName}/${file.zipPath}`, 'utf8');
    const checksum = crc32(data);
    const { dosDate, dosTime } = dosDateTime(deterministicZipDate);

    const localHeader = Buffer.concat([
      uint32(0x04034b50),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(dosTime),
      uint16(dosDate),
      uint32(checksum),
      uint32(data.length),
      uint32(data.length),
      uint16(name.length),
      uint16(0),
      name
    ]);

    const centralHeader = Buffer.concat([
      uint32(0x02014b50),
      uint16(20),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(dosTime),
      uint16(dosDate),
      uint32(checksum),
      uint32(data.length),
      uint32(data.length),
      uint16(name.length),
      uint16(0),
      uint16(0),
      uint16(0),
      uint16(0),
      uint32(0),
      uint32(offset),
      name
    ]);

    localParts.push(localHeader, data);
    centralParts.push(centralHeader);
    offset += localHeader.length + data.length;
  }

  const centralDirectory = Buffer.concat(centralParts);
  const endOfCentralDirectory = Buffer.concat([
    uint32(0x06054b50),
    uint16(0),
    uint16(0),
    uint16(files.length),
    uint16(files.length),
    uint32(centralDirectory.length),
    uint32(offset),
    uint16(0)
  ]);

  fs.writeFileSync(outputFile, Buffer.concat([
    ...localParts,
    centralDirectory,
    endOfCentralDirectory
  ]));

  console.log(`Carpeta ${sourceName} comprimida en ${path.basename(outputFile)}.`);
}

function compressFolders() {
  createStoredZip(path.join(rootDir, 'left4dead2'), path.join(rootDir, 'left4dead2.zip'));
}

function generateFileTree(dir, tree = {}, compressedFiles = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));

  for (const entry of entries) {
    if (exclusions.has(entry.name)) continue;

    const entryPath = path.join(dir, entry.name);

    if (entry.name.endsWith('.zip')) {
      compressedFiles.push(entry.name);
      continue;
    }

    if (entry.isDirectory()) {
      tree[entry.name] = {};
      generateFileTree(entryPath, tree[entry.name], compressedFiles);
    } else if (entry.isFile()) {
      tree[entry.name] = null;
    }
  }

  return { tree, compressedFiles };
}

function writeFileTree() {
  const { tree, compressedFiles } = generateFileTree(rootDir);

  if (Object.keys(tree).length === 0) {
    throw new Error('El arbol de archivos esta vacio. Verifica las exclusiones.');
  }

  ensureDir(filetreeDir);
  fs.writeFileSync(path.join(filetreeDir, 'file-tree.json'), `${JSON.stringify(tree, null, 2)}\n`);
  fs.writeFileSync(path.join(filetreeDir, 'compressed-files.json'), `${JSON.stringify(compressedFiles, null, 2)}\n`);

  console.log('El arbol de archivos ha sido generado correctamente.');
}

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function generateManifest(dir, manifest = {}, basePath = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));

  for (const entry of entries) {
    if (exclusions.has(entry.name)) continue;

    const entryPath = path.join(dir, entry.name);
    const routePath = basePath ? `${basePath}/${entry.name}` : entry.name;

    if (entry.isDirectory()) {
      generateManifest(entryPath, manifest, routePath);
    } else if (entry.isFile()) {
      manifest[toPosixPath(routePath)] = {
        size: fs.statSync(entryPath).size,
        sha256: sha256(entryPath)
      };
    }
  }

  return manifest;
}

function writeManifest() {
  ensureDir(filetreeDir);
  const manifest = generateManifest(rootDir);
  fs.writeFileSync(path.join(filetreeDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  console.log('El manifiesto de archivos ha sido generado correctamente.');
}

function generateRedirects(dir, basePath = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));
  const redirects = [];

  for (const entry of entries) {
    if (exclusions.has(entry.name)) continue;

    const entryPath = path.join(dir, entry.name);
    const routePath = basePath ? `${basePath}/${entry.name}` : entry.name;

    if (entry.isDirectory()) {
      redirects.push(...generateRedirects(entryPath, routePath));
    } else if (entry.isFile()) {
      redirects.push({
        route: `/${toPosixPath(routePath)}`,
        target: '/index.html',
        status: 200
      });
    }
  }

  return redirects;
}

function writeRedirects() {
  ensureDir(filetreeDir);
  const redirects = generateRedirects(rootDir);
  fs.writeFileSync(path.join(filetreeDir, 'redirects.json'), `${JSON.stringify(redirects, null, 2)}\n`);
  console.log('El archivo de redirecciones ha sido generado correctamente.');
}

function writeNoJekyll() {
  fs.closeSync(fs.openSync(path.join(rootDir, '.nojekyll'), 'w'));
}

function main() {
  renderServerMessages();
  compressFolders();
  writeFileTree();
  writeManifest();
  writeRedirects();
  writeNoJekyll();
  console.log('Build completado correctamente.');
}

if (require.main === module) {
  main();
}

module.exports = { main };
