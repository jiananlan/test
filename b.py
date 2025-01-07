import os

def find_mp4_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.webm'):
                print(os.path.join(root, file))

# 指定搜索的目录，当前目录使用'.'
directory = '.'
for i in range(50):
 print('**************')
find_mp4_files(directory)
