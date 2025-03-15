const fs = require('fs');
const path = require('path');
const exclusions = require('./exclusions');  // Importa el Set de exclusiones

const compressedFiles = [];

function generateFileTree(dir, tree = {}) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    if (exclusions.has(file)) return;
    if (file.endsWith('.zip')) {
      compressedFiles.push(file);
      return;
    }

    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      tree[file] = {};
      generateFileTree(filePath, tree[file]);
    } else {
      tree[file] = null;
    }
  });
  return tree;
}

const fileTree = generateFileTree('./');
if (Object.keys(fileTree).length === 0) {
  console.error('El árbol de archivos está vacío. Verifica las rutas de inclusión.');
} else {
  const outputDir = path.join(__dirname, '../filetree');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }
  fs.writeFileSync(path.join(outputDir, 'file-tree.json'), JSON.stringify(fileTree, null, 2));
  fs.writeFileSync(path.join(outputDir, 'compressed-files.json'), JSON.stringify(compressedFiles, null, 2));
  console.log('El árbol de archivos ha sido generado correctamente.');
}
