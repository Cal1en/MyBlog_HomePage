const fs = require('fs');
const path = require('path');

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node fix_spaces.js <markdown_file>");
  process.exit(1);
}

const content = fs.readFileSync(filePath, 'utf8');
const newContent = content.replace(/!\[(.*?)\]\(\/img\/(.*?)\/(.*?)\)/g, (match, alt, folder, filename) => {
  // 如果 folder 里面有实际的空格而不是 %20，把它替换成 %20
  if (folder.includes(' ')) {
    const encodedFolder = encodeURIComponent(folder);
    return `![${alt}](/img/${encodedFolder}/${filename})`;
  }
  return match;
});

fs.writeFileSync(filePath, newContent, 'utf8');
console.log("Fixed spaces in markdown image links.");