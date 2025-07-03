const fs = require('fs').promises;
const path = require('path');
const WebTorrent = require('webtorrent');

async function downloadMagnets() {
  const client = new WebTorrent();
  const outputLog = [];

  // Read magnet links from file
  const input = await fs.readFile('magnet_list.txt', 'utf-8');
  const magnets = input.split('\n').map(line => line.trim()).filter(line => line.startsWith('magnet:'));
  
  // Create downloads directory if it doesn't exist
  await fs.mkdir('downloads', { recursive: true });

  for (const magnet of magnets) {
    console.log(`Starting download: ${magnet}`);
    outputLog.push(`Starting download: ${magnet}`);

    try {
      // Download with progress tracking
      await new Promise((resolve, reject) => {
        client.add(magnet, { path: './downloads' }, torrent => {
          // Log torrent metadata when available
          console.log(`Torrent name: ${torrent.name}`);
          outputLog.push(`Torrent name: ${torrent.name}`);

          // Track progress
          torrent.on('download', () => {
            const progress = (torrent.progress * 100).toFixed(2);
            const speed = (torrent.downloadSpeed / 1024 / 1024).toFixed(2); // MB/s
            const downloaded = (torrent.downloaded / 1024 / 1024).toFixed(2); // MB
            const total = (torrent.length / 1024 / 1024).toFixed(2); // MB
            console.log(`Progress: ${progress}% | Speed: ${speed} MB/s | Downloaded: ${downloaded} MB / ${total} MB`);
            outputLog.push(`Progress: ${progress}% | Speed: ${speed} MB/s | Downloaded: ${downloaded} MB / ${total} MB`);
          });

          torrent.on('done', () => {
            console.log(`Completed: ${magnet}`);
            outputLog.push(`Completed: ${magnet}`);
            resolve();
          });

          torrent.on('error', err => {
            console.error(`Error downloading ${magnet}: ${err.message}`);
            outputLog.push(`❌ Error downloading ${magnet}: ${err.message}`);
            reject(err);
          });
        });
      });
    } catch (err) {
      console.error(`Failed to download: ${magnet}`);
      outputLog.push(`❌ Failed to download: ${magnet}`);
    }
  }

  // Write logs to file
  await fs.writeFile('output.txt', outputLog.join('\n'));

  // Clean up WebTorrent client
  client.destroy();
}

downloadMagnets().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
