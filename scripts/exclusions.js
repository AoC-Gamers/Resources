// exclusions.js
// Union de todas las exclusiones necesarias
const exclusions = new Set([
    // Git
    '.git',
    '.github',
    '.gitignore',
    '.gitkeep',
    '.nojekyll',
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
    '.node-version',
    '.nvmrc',
    'package-lock.json',
    'package.json',

    // Scripts
    'build.sh',
    'build.ps1',
    'scripts',
    'filetree',

    // Others
    'index.html',
    'robots.txt',
    'CNAME',
    'favicon.ico'
  ]);
  
  module.exports = exclusions;
