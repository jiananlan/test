const WebTorrent = require('webtorrent');
const fs = require('fs');
const path = require('path');

const client = new WebTorrent();
const savePath = path.join(__dirname, 'downloads');
const magnets = fs.readFileSync('magnet_list.txt', 'utf-8')
  .split('\n')
  .map(line => line.trim())
  .filter(line => line.startsWith('magnet:'));

if (!fs.existsSync(savePath)) fs.mkdirSync(savePath);

const outputLog = [];

function downloadOne(magnet, callback) {
  console.log(`开始下载: ${magnet}`);
  client.add(magnet, { path: savePath }, torrent => {
    const interval = setInterval(() => {
      const percent = (torrent.progress * 100).toFixed(2);
      const speed = (torrent.downloadSpeed / 1024).toFixed(2);
      const peers = torrent.numPeers;
      process.stdout.write(`\r下载进度: ${percent}% | 速度: ${speed} KB/s | Peers: ${peers}`);
    }, 1000);

    torrent.on('done', () => {
      clearInterval(interval);
      console.log(`\n✅ 下载完成: ${torrent.name}`);
      outputLog.push(`成功下载: ${torrent.name} | ${magnet}`);
      callback();
    });

    torrent.on('error', err => {
      clearInterval(interval);
      console.error(`\n❌ 下载失败: ${err.message}`);
      outputLog.push(`失败: ${magnet} | ${err.message}`);
      callback();
    });
  });
}

function downloadAll(index = 0) {
  if (index >= magnets.length) {
    fs.writeFileSync('output.txt', outputLog.join('\n'));
    console.log('\n📄 所有任务完成，结果写入 output.txt');
    client.destroy();
    return;
  }

  downloadOne(magnets[index], () => downloadAll(index + 1));
}

downloadAll();
