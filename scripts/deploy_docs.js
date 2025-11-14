const fs = require('fs');
const path = require('path');

const src = path.resolve(__dirname, '..', 'dist');
const dest = path.resolve(__dirname, '..', 'docs');

function rmrf(directory) {
  if (!fs.existsSync(directory)) return;
  for (const file of fs.readdirSync(directory)) {
    const cur = path.join(directory, file);
    if (fs.lstatSync(cur).isDirectory()) {
      rmrf(cur);
    } else {
      fs.unlinkSync(cur);
    }
  }
  fs.rmdirSync(directory);
}

function copyDir(srcDir, destDir) {
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
  for (const file of fs.readdirSync(srcDir)) {
    const cur = path.join(srcDir, file);
    const target = path.join(destDir, file);
    if (fs.lstatSync(cur).isDirectory()) {
      copyDir(cur, target);
    } else {
      fs.copyFileSync(cur, target);
    }
  }
}

try {
  rmrf(dest);
  copyDir(src, dest);
  console.log('Copied dist -> docs');
} catch (err) {
  console.error('Failed to copy dist -> docs', err);
  process.exit(1);
}
