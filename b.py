from pytube import YouTube

# 输入视频URL
video_url = 'https://www.youtube.com/watch?v=4ktJ1Xbudpc'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# 创建YouTube对象
yt = YouTube(video_url,headers=headers)

# 获取最高质量的视频流
video_stream = yt.streams.get_highest_resolution()

# 下载视频到当前目录
video_stream.download(filename='a.mp4')

print("视频下载完成")
