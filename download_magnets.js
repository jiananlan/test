const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

const input = fs.readFileSync('magnet_list.txt', 'utf-8');
const magnets = input.split('\n').map(line => line.trim()).filter(line => line.startsWith('magnet:'));

const outputLog = [];

for (const magnet of magnets) {
  try {
    console.log(`开始下载: ${magnet}`);
    execSync(`npx webtorrent download "${magnet}" --out downloads --quiet`, { stdio: 'inherit' });
    outputLog.push(`成功下载: ${magnet}`);
  } catch (err) {
    outputLog.push(`❌ 下载失败: ${magnet}`);
  }
}

fs.writeFileSync('output.txt', outputLog.join('\n'));
