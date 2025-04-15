import time
import os
while True:
  # 获取 secret 值
  my_secret = os.environ['TEST_SECRET']
  
  # 使用 secret（以下为示例，请勿打印真实 secret）
  print("Secret loaded successfully.",my_secret)  # 删掉敏感输出
  time.sleep(1)
