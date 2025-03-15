const fs = require('fs');
const path = require('path');
const exclusions = require('./exclusions');  // Importa el Set de exclusiones

function generateRedirects(dir, basePath = '') {
  const files = fs.readdirSync(dir);
  const redirects = [];

  files.forEach(file => {
    if (exclusions.has(file)) return;

    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      redirects.push(...generateRedirects(filePath, path.join(basePath, file)));
    } else {
      const route = path.join(basePath, file).replace(/\\/g, '/');
      redirects.push({ route: `/${route}`, target: '/index.html', status: 200 });
    }
  });

  return redirects;
}

const redirects = generateRedirects('./');
const outputDir = path.join(__dirname, '../filetree');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir);
}
fs.writeFileSync(path.join(outputDir, 'redirects.json'), JSON.stringify(redirects, null, 2));
console.log('El archivo de redirecciones ha sido generado correctamente.');
