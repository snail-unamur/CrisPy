const fs = require("node:fs");
const path = require("node:path");

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

// Copy analyzer
const analyzerSrc = path.resolve(__dirname, "../../analyzer/src");
const analyzerDest = path.resolve(__dirname, "../analyzer");
if (fs.existsSync(analyzerDest)) fs.rmSync(analyzerDest, { recursive: true });
copyDir(analyzerSrc, analyzerDest);
console.log("Analyzer copied to extension/analyzer/");

// Copy rule docs
const docsSrc = path.resolve(__dirname, "../../docs/pages/rules");
const docsDest = path.resolve(__dirname, "../docs/rules");
if (fs.existsSync(docsDest)) fs.rmSync(docsDest, { recursive: true });
copyDir(docsSrc, docsDest);
console.log("Docs copied to extension/docs/rules/");
