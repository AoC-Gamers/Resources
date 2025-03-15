const fs = require('fs');
const path = require('path');
const exclusions = require('./exclusions');  // Importa el Set de exclusiones

function generateRedirects(dir, basePath = '') {
  const files = fs.readdirSync(dir);
  let redirects = '';

  files.forEach(file => {
    if (exclusions.has(file)) return;

    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      redirects += generateRedirects(filePath, path.join(basePath, file));
    } else {
      const route = path.join(basePath, file).replace(/\\/g, '/');
      redirects += `/${route} /index.html 200\n`;
    }
  });

  return redirects;
}

const redirects = generateRedirects('./');
fs.writeFileSync('_redirects', redirects);
console.log('El archivo de redirecciones ha sido generado correctamente.');
