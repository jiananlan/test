from bs4 import BeautifulSoup
import requests

# GitHub仓库信息
username = 'jiananlan'  # GitHub用户名
repo = 'test'  # 仓库名
file_path = 'test.txt'  # 文件路径
branch = 'main'  # 分支名

# API的基础URL
api_url = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}?ref={branch}'


# 获取文件内容
def get_file_content():
    headers = {'Authorization': f'token {token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        file_info = response.json()
        content = base64.b64decode(file_info['content']).decode('utf-8')
        return content
    else:
        print(f"Error fetching file: {response.status_code}")
        return None

for i in range(50000):
    import time
    time.sleep(5)
    print(get_file_content())
