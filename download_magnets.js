import WebTorrent from 'webtorrent';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const client = new WebTorrent();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const savePath = path.join(__dirname, 'downloads');
if (!fs.existsSync(savePath)) fs.mkdirSync(savePath);

// 读取磁力链接列表（过滤空行和非磁力链接）
const fileContent = fs.readFileSync('magnet_list.txt', 'utf-8');
const magnets = fileContent
  .split('\n')
  .map(line => line.trim())
  .filter(line => line.startsWith('magnet:'));

if (magnets.length === 0) {
  console.error('❌ 未找到有效的磁力链接，请检查 magnet_list.txt');
  process.exit(1);
}

console.log(`📥 共读取 ${magnets.length} 个磁力链接`);

const outputLog = [];

/**
 * 从磁力链接中提取 infoHash 和 tracker 列表
 * @param {string} magnet - 完整磁力链接
 * @returns {{ infoHash: string, trackers: string[] } | null}
 */
function parseMagnet(magnet) {
  const infoHashMatch = magnet.match(/btih:([a-f0-9]{40})/i);
  if (!infoHashMatch) return null;

  const infoHash = infoHashMatch[1].toLowerCase();
  const trackers = [];
  const trRegex = /[&?]tr=([^&]+)/g;
  let match;
  while ((match = trRegex.exec(magnet)) !== null) {
    trackers.push(decodeURIComponent(match[1]));
  }
  return { infoHash, trackers };
}

/**
 * 下载单个磁力链接
 * @param {string} magnet - 磁力链接字符串
 * @param {Function} callback - 完成或失败后的回调
 */
function downloadOne(magnet, callback) {
  const parsed = parseMagnet(magnet);
  if (!parsed) {
    console.error(`❌ 无效磁力链接（无 btih）: ${magnet}`);
    outputLog.push(`失败: ${magnet} | 无法提取 infoHash`);
    callback();
    return;
  }

  const { infoHash, trackers } = parsed;
  console.log(`🔽 开始下载: ${magnet} (infoHash: ${infoHash}, trackers: ${trackers.length})`);

  const options = { path: savePath };
  if (trackers.length > 0) {
    options.announce = trackers; // 将提取的 tracker 加入
  }

  client.add(infoHash, options, (torrent) => {
    const interval = setInterval(() => {
      const percent = (torrent.progress * 100).toFixed(2);
      const speed = (torrent.downloadSpeed / 1024).toFixed(2);
      const peers = torrent.numPeers;
      process.stdout.write(`\r📊 进度: ${percent}% | 速度: ${speed} KB/s | Peers: ${peers}`);
    }, 1000);

    torrent.on('done', () => {
      clearInterval(interval);
      console.log(`\n✅ 下载完成: ${torrent.name}`);
      outputLog.push(`成功下载: ${torrent.name} | ${magnet}`);
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

/**
 * 顺序执行所有下载任务
 * @param {number} index - 当前任务索引
 */
function downloadAll(index = 0) {
  if (index >= magnets.length) {
    fs.writeFileSync('output.txt', outputLog.join('\n'));
    console.log('\n📄 所有任务完成，结果已写入 output.txt');
    client.destroy();
    return;
  }

  downloadOne(magnets[index], () => downloadAll(index + 1));
}

// 启动下载
downloadAll();
