import os
from utils.logger import Logger

class Overwriter:
    def __init__(self):
         self.logger = Logger()

    def secure_delete(self, file_path, passes=3):

        if not os.path.isfile(file_path):
            print(f"[!] Skipping (not a file): {file_path}")
            self.logger.log(file_path, passes, success=False)
            return False

        try:
            file_size = os.path.getsize(file_path)

            with open(file_path, 'r+b') as f:
                for i in range(passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                    print(f"  → Pass {i+1} complete on: {file_path}")

            os.remove(file_path)
            print(f"[✓] Securely erased: {file_path}")
            self.logger.log(file_path, passes, success=True)
            return True

        except Exception as e:
            print(f"[X] Error erasing {file_path}: {e}")
            self.logger.log(path, passes, success=False)
            return False

    def process_path(self, path, passes=3):
        """Process a file or all files in a folder."""
        if os.path.isfile(path):
            self.secure_delete(path, passes)

        elif os.path.isdir(path):
            print(f"[→] Entering folder: {path}")
            for root, dirs, files in os.walk(path):
                for name in files:
                    file_path = os.path.join(root, name)
                    self.secure_delete(file_path, passes)
        else:
            print(f"[!] Invalid path: {path}")
