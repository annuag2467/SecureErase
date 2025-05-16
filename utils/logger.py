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
                writer.writerow(['Timestamp', 'File Path', 'Passes', 'Success', 'Verified'])


    def log(self, file_path, passes, success, verified):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Convert success boolean to string
            if success:
              success_str = 'Yes'
            else:
              success_str = 'No'

            # Convert verified to string
            if verified is None:
               verified_str = 'N/A'
            elif verified:
               verified_str = 'Yes'
            else:
               verified_str = 'No'


            with open(self.log_file, mode='a', newline='') as file:
               writer = csv.writer(file)
               writer.writerow([timestamp, file_path, passes, success_str, verified_str])

            print(f"[LOG] {timestamp} | File: {file_path} | Passes: {passes} | Success: {success_str} | Verified: {verified_str}")