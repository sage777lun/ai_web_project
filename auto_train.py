import os
import time

while True:
    print("⏳ 檢查新訓練數據...")
    os.system("python train_gpt2.py")  
    time.sleep(3600)  # **每 1 小時訓練一次**