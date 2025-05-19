import csv
import os
from datetime import datetime

class Logger:
    def _init_(self, log_file='logs/erasure_log.csv'):
        self.log_file = log_file

        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)


        if not os.path.isfile(self.log_file):
            with open(self.log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'File Path', 'Passes', 'Success'])


    def log(self, file_path, passes, success):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
            if success:
              success_str = 'Yes'
            else:
              success_str = 'No'

            with open(self.log_file, mode='a', newline='') as file:
               writer = csv.writer(file)
               writer.writerow([timestamp, file_path, passes, success_str])

            print(f"[LOG] {timestamp} | File: {file_path} | Passes: {passes} | Success: {success_str}")