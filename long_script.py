import time
import os
from datetime import datetime
start_time = time.time()

while True:
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Current Date and Time:", current_datetime)
    elapsed_time = time.time() - start_time
    print(f"Elapsed Time (seconds since start): {elapsed_time:.2f} seconds")
    my_secret = os.environ['TEST_SECRET']
    print("Secret loaded successfully.")
    print("Secret length:", len(my_secret)) 
    time.sleep(5)
