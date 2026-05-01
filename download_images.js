const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node download_images.js <markdown_file>");
  process.exit(1);
}

const content = fs.readFileSync(filePath, 'utf8');
const postName = path.basename(filePath, '.md');

// 获取当前 md 文件相对于 source/_posts 的相对路径
// 比如 source/_posts/Kerry/01_渲染管线概述.md -> Kerry
const postsDir = path.join(__dirname, 'source', '_posts');
const relativeDir = path.relative(postsDir, path.dirname(filePath));

// 在 source/img 下复刻相对路径，并带上文章同名文件夹
const imgDir = path.join(__dirname, 'source', 'img', relativeDir, postName);

if (!fs.existsSync(imgDir)) {
  fs.mkdirSync(imgDir, { recursive: true });
}

let newContent = content;
const regex = /!\[([^\]]*)\]\((https?:\/\/[^\)]+)\)/g;

let match;
const downloads = [];

while ((match = regex.exec(content)) !== null) {
  const alt = match[1];
  const url = match[2];
  
  let filename = url.split('/').pop().split('?')[0];
  if (!filename || !filename.includes('.')) {
    filename = Date.now() + '.png';
  }
  
  const localPath = path.join(imgDir, filename);
  // 使用绝对路径，并在 URL 中拼接多级相对目录
  // 注意要把 Windows 的反斜杠 \ 替换为 URL 的正斜杠 /
  let urlRelativeDir = relativeDir.split(path.sep).join('/');
  if (urlRelativeDir) {
    urlRelativeDir += '/';
  }
  const markdownPath = `/img/${urlRelativeDir}${postName}/${filename}`;
  
  downloads.push({ url, localPath, originalUrl: url, markdownPath });
}

if (downloads.length === 0) {
  console.log("No images found.");
  process.exit(0);
}

console.log(`Found ${downloads.length} images.`);

async function downloadImage(url, dest) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.yuque.com/'
      }
    };
    client.get(url, options, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`Failed to download: ${res.statusCode}`));
        return;
      }
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
}

async function run() {
  for (const dl of downloads) {
    console.log(`Downloading ${dl.url}...`);
    try {
      await downloadImage(dl.url, dl.localPath);
      newContent = newContent.replace(dl.originalUrl, dl.markdownPath);
    } catch (e) {
      console.error(`Error downloading ${dl.url}:`, e.message);
    }
  }
  
  fs.writeFileSync(filePath, newContent, 'utf8');
  console.log("Done! Markdown file updated.");
}

run();
