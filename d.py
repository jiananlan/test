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


video_url = 'https://www.youtube.com/watch?v=42v4Xm6bv50'  # 替换为实际的YouTube视频链接
cookies_file = 'cookies.txt'  # 替换为你自己的cookies文件路径
download_video_with_cookies(video_url, cookies_file)

###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################
###########################################
##################下载部分##################
###########################################

# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#
# -----------------------------------------#


from biliup.plugins.bili_webup import BiliBili, Data
import os

video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm']

video_files = []


def find_video_files():
    global video_files, video_extensions
    for root, dirs, files in os.walk('./'):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in video_extensions:
                video_files.append(os.path.join(root, file))
    print(video_files)
    return


find_video_files()
video = Data()
video.title = video_files[0].split('/')[-1].split('.')[0] + "  [3分钟航空]"
print(video.title)
video.desc = '3分钟航空-3 Minutes of Aviation   ' + video.title.split('[')[0]
video.source = video_url
video.tid = 232
video.set_tag(['三分钟航空', '3 Minutes of Aviation', '航空', '飞机', '飞行'])
with BiliBili(video) as bili:
    c = {"bili-jct": "6d6928492ee639acb3dac9e72fdf8a60",
         'DedeUserID__ckMd5': '59d328699a0dc28d',
         'DedeUserID': '3546702273317241',
         'SESSDATA': '46ab82d5%2C1752491094%2C1c29b%2A12CjABitUFFvcnSAUTzSL1NfajiCv2J4xjpUtfCyzuyFRy0yHpKIiiQanAEivZqpywK7ESVmdvd1lRRXUyV25yTVpVTXUzeVZpN29NQXFKeFF2UWVDQU5uX29GOFpBWEVmTkZObDRxWHpXejEzYmpGYzlRR2I1QUcwQ0xNRDI2SmlrbWg2V2hpQ2FBIIEC'}
    bili.login("bili.cookie", {
        'cookies': c, 'access_token': 'your access_key'})
    for file in video_files:
        video_part = bili.upload_file(file)  # 上传视频
        video.append(video_part)  # 添加已经上传的视频
    # video.cover = bili.cover_up('/cover_path').replace('http:', '')
    try:
        ret = bili.submit()
        # 提交视频
    except Exception as e:
        print(e)
