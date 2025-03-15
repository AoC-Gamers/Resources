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
    'build.sh',
    'scripts',
    'filetree',

    // Others
    'index.html',
    'robots.txt',
    'CNAME',
    'favicon.ico'
  ]);
  
  module.exports = exclusions;
