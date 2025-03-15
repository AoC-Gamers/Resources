// exclusions.js
// Union de todas las exclusiones necesarias
const exclusions = new Set([
    // Git
    '.git',
    '.gitignore',
    '.vscode',
    'README.md',

    // jekyll
    '_config.yml',
    '_layouts',
    '.jekyll-cache',
    '_site',
    'Gemfile',
    'Gemfile.lock',
    '_redirects',

    // Node
    'package-lock.json',
    'package.json',

    // Scripts
    'compressFolders.sh',
    'file-tree.json',
    'generateFileTree.js',
    'build.sh',
    'compressed-files.json',
    'generateRedirects.js',
    'exclusions.js',

    // Others
    'index.html',
    'robots.txt',
    'CNAME',
    'favicon.ico'
  ]);
  
  module.exports = exclusions;
  