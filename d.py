import yt_dlp

def download_video_with_cookies(url, cookies_file, output_path='downloads'):
    # 配置下载选项
    ydl_opts = {
        'format': 'best',  # 下载最佳质量的视频
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # 设置下载后的文件保存路径和命名
        'cookiefile': cookies_file,  # 使用提供的cookies文件
    }

    # 使用yt-dlp下载视频
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=IWSN0Sc3IrY'  # 替换为实际的YouTube视频链接
    cookies_file = 'cookies.txt'  # 替换为你自己的cookies文件路径
    download_video_with_cookies(video_url, cookies_file)