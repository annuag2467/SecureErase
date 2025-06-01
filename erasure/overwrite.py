import os
from utils.logger import Logger


class Overwriter:
    def __init__(self, logger=None):
        self.logger = logger or Logger()


    def overwrite_and_delete(self, file_path, passes=3):
        """Securely overwrite and delete a single file"""
        
        # Validate the file path
        if not os.path.exists(file_path):
            print(f"[!] File does not exist: {file_path}")
            self.logger.log(file_path, passes, success=False)
            return False

        if not os.path.isfile(file_path):
            print(f"[!] Skipping (not a file): {file_path}")
            self.logger.log(file_path, passes, success=False)
            return False


        try:
            file_size = os.path.getsize(file_path)
            
            # Handle empty files
            if file_size == 0:
                print(f"[i] File is empty, just deleting: {file_path}")
                os.remove(file_path)
                print(f"[✓] Deleted empty file: {file_path}")
                self.logger.log(file_path, passes, success=True)
                return True

            print(f"[→] Overwriting {file_path} ({file_size} bytes) with {passes} passes...")

            with open(file_path, 'r+b') as f:
                for i in range(passes):
                    f.seek(0)
                    # Write random data
                    random_data = os.urandom(file_size)
                    f.write(random_data)
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk
                    print(f"  → Pass {i+1}/{passes} complete")

            # Final step: remove the file
            os.remove(file_path)
            print(f"[✓] Securely erased: {file_path}")
            self.logger.log(file_path, passes, success=True)
            return True

        except PermissionError:
            print(f"[X] Permission denied: {file_path}")
            self.logger.log(file_path, passes, success=False)
            return False
        except OSError as e:
            print(f"[X] OS error erasing {file_path}: {e}")
            self.logger.log(file_path, passes, success=False)
            return False
        except Exception as e:
            print(f"[X] Unexpected error erasing {file_path}: {e}")
            self.logger.log(file_path, passes, success=False)
            return False

    def process_path(self, path, passes=3):
        """Process a file or all files in a folder."""
        if not os.path.exists(path):
            print(f"[!] Path does not exist: {path}")
            return False

        if os.path.isfile(path):
            return self.overwrite_and_delete(path, passes)

        elif os.path.isdir(path):
            print(f"[→] Processing directory: {path}")
            success_count = 0
            total_count = 0
            
            try:
                for root, dirs, files in os.walk(path, topdown=False):
                    # Process files first
                    for name in files:
                        file_path = os.path.join(root, name)
                        total_count += 1
                        if self.overwrite_and_delete(file_path, passes):
                            success_count += 1
                    
                    # Then try to remove empty directories
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        try:
                            os.rmdir(dir_path)
                            print(f"[✓] Removed empty directory: {dir_path}")
                        except OSError:
                            print(f"[!] Could not remove directory (not empty?): {dir_path}")
                
                # Finally, try to remove the root directory
                try:
                    os.rmdir(path)
                    print(f"[✓] Removed directory: {path}")
                except OSError:
                    print(f"[!] Could not remove root directory: {path}")
                
                print(f"[i] Directory processing complete: {success_count}/{total_count} files processed")
                return success_count == total_count
                
            except Exception as e:
                print(f"[X] Error processing directory {path}: {e}")
                return False
        else:
            print(f"[!] Invalid path (not a file or directory): {path}")
            return False

