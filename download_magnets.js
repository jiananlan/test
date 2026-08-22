import WebTorrent from 'webtorrent';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const client = new WebTorrent();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const savePath = path.join(__dirname, 'downloads');
if (!fs.existsSync(savePath)) fs.mkdirSync(savePath, { recursive: true });

// ========== 1. 读取并过滤磁力链接 ==========
let magnets = [];
try {
  const content = fs.readFileSync('magnet_list.txt', 'utf-8');
  magnets = content
    .split(/\r?\n/)          // 兼容 Windows/Unix 换行
    .map(line => line.trim())
    .filter(line => line.startsWith('magnet:'));
} catch (err) {
  console.error('❌ 读取 magnet_list.txt 失败:', err.message);
  process.exit(1);
}

if (magnets.length === 0) {
  console.error('❌ 未找到任何磁力链接，请检查文件内容');
  process.exit(1);
}

console.log(`📥 共读取 ${magnets.length} 个磁力链接`);
magnets.forEach((m, i) => console.log(`  [${i}] ${m}`));

const outputLog = [];

// ========== 2. 从磁力链接中提取 infoHash 和 trackers ==========
function parseMagnet(magnet) {
  // 匹配 btih: 后跟 40 个十六进制字符（不区分大小写）
  const match = magnet.match(/btih:([a-f0-9]{40})/i);
  if (!match) return null;
  const infoHash = match[1].toLowerCase();

  // 提取所有 tr= 参数
  const trackers = [];
  const trRegex = /[&?]tr=([^&]+)/g;
  let t;
  while ((t = trRegex.exec(magnet)) !== null) {
    trackers.push(decodeURIComponent(t[1]));
  }
  return { infoHash, trackers };
}

// ========== 3. 下载单个任务（带防呆保护） ==========
function downloadOne(magnet, callback) {
  console.log(`\n🔍 正在解析: ${magnet}`);

  const parsed = parseMagnet(magnet);
  if (!parsed) {
    console.error(`❌ 无法提取 infoHash，跳过`);
    outputLog.push(`跳过: ${magnet} | 无法提取 infoHash`);
    callback();
    return;
  }

  const { infoHash, trackers } = parsed;
  console.log(`✅ 解析成功: infoHash = ${infoHash}, trackers = ${trackers.length} 个`);

  // *** 关键：二次确认 infoHash 不是 undefined/null/非字符串 ***
  if (typeof infoHash !== 'string' || infoHash.length !== 40) {
    console.error(`❌ infoHash 无效 (${infoHash})，跳过`);
    outputLog.push(`跳过: ${magnet} | infoHash 无效`);
    callback();
    return;
  }

  // 构造选项
  const options = { path: savePath };
  if (trackers.length > 0) {
    options.announce = trackers;
  }

  console.log(`⬇️  开始下载 (infoHash: ${infoHash}) ...`);

  // *** 确保第一个参数是 infoHash 字符串，绝不是 undefined ***
  client.add(infoHash, options, (torrent) => {
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

  // 额外捕获 client.add 的同步异常（理论不会发生，但以防万一）
  // 实际上 add 是同步注册事件，不会抛错
}

// ========== 4. 顺序执行 ==========
function downloadAll(index = 0) {
  if (index >= magnets.length) {
    fs.writeFileSync('output.txt', outputLog.join('\n'));
    console.log('\n📄 所有任务完成，结果写入 output.txt');
    client.destroy();
    return;
  }

  downloadOne(magnets[index], () => downloadAll(index + 1));
}

// ========== 启动 ==========
downloadAll();
