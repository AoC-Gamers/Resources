const fs = require('fs');
const path = require('path');

const exclusions = ['node_modules', '.git', 'file-tree.json', 'generateFileTree.js', '.theme', 'aoc_servermessage', 'robots.txt'];

function generateFileTree(dir, tree = {}) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        if (exclusions.includes(file)) return;

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
fs.writeFileSync('file-tree.json', JSON.stringify(fileTree, null, 2));