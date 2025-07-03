import libtorrent as lt
import time
import os

save_path = "downloads"
os.makedirs(save_path, exist_ok=True)

with open("magnet_list.txt", "r") as f:
    magnets = [line.strip() for line in f if line.strip().startswith("magnet:")]

results = []

ses = lt.session()
ses.listen_on(6881, 6891)

for uri in magnets:
    print(f"开始下载: {uri}")
    params = lt.parse_magnet_uri(uri)
    params.save_path = save_path
    handle = ses.add_torrent(params)

    print("正在获取元数据…")
    while not handle.has_metadata():
        time.sleep(1)

    print("正在下载:", handle.name())
    while not handle.is_seed():
        s = handle.status()
        print(f"\r进度: {s.progress * 100:.2f}%", end="")
        time.sleep(1)

    print(f"\n下载完成: {handle.name()}")
    results.append(f"{handle.name()} | 来自: {uri}")

# 写入输出日志
with open("output.txt", "w") as out:
    out.write("\n".join(results))
