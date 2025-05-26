import csv
import os
from datetime import datetime


class Logger:
    def __init__(self, log_file='logs/erasure_log.csv'):
        self.log_file = log_file
        self._initialize_log_file()

    def _initialize_log_file(self):
        """Initialize the log file and create directory if needed"""
        log_dir = os.path.dirname(self.log_file)
        
        # Create log directory if it doesn't exist
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                print(f"[!] Warning: Could not create log directory {log_dir}: {e}")
                # Fallback to current directory
                self.log_file = 'erasure_log.csv'

        # Create log file with headers if it doesn't exist
        if not os.path.isfile(self.log_file):
            try:
                with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Timestamp', 'File Path', 'Passes', 'Success', 'File Size'])
            except IOError as e:
                print(f"[!] Warning: Could not initialize log file {self.log_file}: {e}")

    def log(self, file_path, passes, success, file_size=None):
        """Log an erasure operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_str = 'Yes' if success else 'No'
        
        # Get file size if not provided and file still exists
        if file_size is None:
            try:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                else:
                    file_size = 'N/A'
            except OSError:
                file_size = 'N/A'

        try:
            with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, file_path, passes, success_str, file_size])
        except IOError as e:
            print(f"[!] Warning: Could not write to log file: {e}")

        # Also print to console for immediate feedback
        print(f"[LOG] {timestamp} | File: {file_path} | Passes: {passes} | Success: {success_str}")

    def get_log_summary(self):
        """Get a summary of logged operations"""
        if not os.path.exists(self.log_file):
            return {"total": 0, "successful": 0, "failed": 0}
        
        try:
            with open(self.log_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                total = 0
                successful = 0
                
                for row in reader:
                    total += 1
                    if row.get('Success', '').lower() == 'yes':
                        successful += 1
                
                return {
                    "total": total,
                    "successful": successful, 
                    "failed": total - successful
                }
        except IOError as e:
            print(f"[!] Could not read log file for summary: {e}")
            return {"total": 0, "successful": 0, "failed": 0}