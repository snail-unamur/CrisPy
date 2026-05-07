const fs = require("node:fs");
const path = require("node:path");

const src = path.resolve(__dirname, "../../analyzer/src");
const dest = path.resolve(__dirname, "../analyzer");

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const srcPath = path.join(from, entry.name);
    const destPath = path.join(to, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Clean previous copy
if (fs.existsSync(dest)) fs.rmSync(dest, { recursive: true });

copyDir(src, dest);
console.log("Analyzer copied to extension/analyzer/");
