import WebTorrent from 'webtorrent';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const client = new WebTorrent();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const savePath = path.join(__dirname, 'downloads');
if (!fs.existsSync(savePath)) fs.mkdirSync(savePath, { recursive: true });

// 读取磁力链接
let magnets = [];
try {
  const content = fs.readFileSync('magnet_list.txt', 'utf-8');
  magnets = content
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(line => line.startsWith('magnet:'));
} catch (err) {
  console.error('❌ 读取文件失败:', err.message);
  process.exit(1);
}

if (magnets.length === 0) {
  console.error('❌ 未找到有效的磁力链接');
  process.exit(1);
}

console.log(`📥 共读取 ${magnets.length} 个磁力链接`);
magnets.forEach((m, i) => console.log(`  [${i}] ${m}`));

const outputLog = [];

/**
 * 从磁力链接中提取 infoHash 和 trackers
 */
function parseMagnet(magnet) {
  const match = magnet.match(/btih:([a-f0-9]{40})/i);
  if (!match) return null;
  const infoHash = match[1].toLowerCase();

  const trackers = [];
  const trRegex = /[&?]tr=([^&]+)/g;
  let t;
  while ((t = trRegex.exec(magnet)) !== null) {
    trackers.push(decodeURIComponent(t[1]));
  }
  return { infoHash, trackers };
}

function downloadOne(magnet, callback) {
  console.log(`\n🔍 解析: ${magnet}`);
  const parsed = parseMagnet(magnet);
  if (!parsed) {
    console.error(`❌ 无效磁力链接（无 btih）`);
    outputLog.push(`跳过: ${magnet} | 无 btih`);
    callback();
    return;
  }

  const { infoHash, trackers } = parsed;
  console.log(`✅ infoHash = ${infoHash}, trackers = ${trackers.length} 个`);

  // ===== 核心修复：构造 torrent 对象，不依赖字符串解析 =====
  const torrentOpts = {
    infoHash: infoHash,
    ...(trackers.length > 0 && { announce: trackers })
  };

  console.log(`⬇️  开始下载 (对象方式)`);

  // 传入对象，而不是字符串
  client.add(torrentOpts, { path: savePath }, (torrent) => {
    console.log(`✅ Torrent 已添加: ${torrent.infoHash}`);

    const interval = setInterval(() => {
      const percent = (torrent.progress * 100).toFixed(2);
      const speed = (torrent.downloadSpeed / 1024).toFixed(2);
      const peers = torrent.numPeers;
      process.stdout.write(`\r📊 进度: ${percent}% | 速度: ${speed} KB/s | Peers: ${peers}`);
    }, 1000);

    torrent.on('done', () => {
      clearInterval(interval);
      console.log(`\n✅ 下载完成: ${torrent.name}`);
      outputLog.push(`成功: ${torrent.name} | ${magnet}`);
      callback();
    });

    torrent.on('error', (err) => {
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
