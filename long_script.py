while True:
  from datetime import datetime
  current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print("Current Date and Time:", current_datetime)
  import time 
  time.sleep(5)
