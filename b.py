
# 输入视频链接
url = 'https://www.youtube.com/watch?v=4ktJ1Xbudpc'

import yt_dlp
 # 替换为你的视频链接

ydl_opts = {
    'outtmpl': r'a.mp4',  # 下载的视频保存的路径和文件名
    'format': 'bestvideo+bestaudio/best',  # 下载最佳质量的视频和音频
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
