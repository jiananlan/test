from pytube import YouTube

# 输入视频URL
video_url = 'https://www.youtube.com/watch?v=4ktJ1Xbudpc'

# 创建YouTube对象
yt = YouTube(video_url)

# 获取最高质量的视频流
video_stream = yt.streams.get_highest_resolution()

# 下载视频到当前目录
video_stream.download(filename='a.mp4')

print("视频下载完成")
