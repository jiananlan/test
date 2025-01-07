from pytube import YouTube
from pytube.request import get, on_progress
import requests

# 修改请求头以模拟浏览器行为
def custom_get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text

# 使用自定义的get请求替代默认的pytube.get
YouTube._get = custom_get

# 输入视频URL
video_url = 'https://www.youtube.com/watch?v=4ktJ1Xbudpc'

# 创建YouTube对象
yt = YouTube(video_url)

# 获取最高质量的视频流
video_stream = yt.streams.get_highest_resolution()

# 下载视频
video_stream.download()

print("视频下载完成")

