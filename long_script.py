while True:
  from datetime import datetime
  current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print("Current Date and Time:", current_datetime)
  import time 
  time.sleep(5)
  import os
  my_secret = os.environ['TEST_SECRET']
  
  # 使用 secret（以下为示例，请勿打印真实 secret）
  print("Secret loaded successfully.",my_secret,str(my_secret),my_secret[0],my_secret=="test")  # 删掉敏感输出
