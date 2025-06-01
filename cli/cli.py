from utils.logger import Logger
from erasure.overwrite import Overwriter
import argparse


class SecureEraseCLI:
    def __init__(self):
        self.logger = Logger()
        self.overwriter = Overwriter(self.logger)
        self.parser = argparse.ArgumentParser(description="Secure Erase Tool")
        self.setup_arguments()
    
    def setup_arguments(self):
        self.parser.add_argument("paths", nargs="*", help="Files or folders to erase")
        self.parser.add_argument("--passes", type=int, default=None, help="Number of overwrite passes")

    def get_paths_interactively(self):
        print("\n[Interactive Mode]")
        print("No file paths provided. Let's collect them now.")
        raw_paths = input("Enter one or more paths (comma-separated): ").strip()
        
        if not raw_paths:
            print("No paths provided. Exiting.")
            return []
            
        paths = raw_paths.split(",")
        cleaned_paths = []
        for p in paths:
            p = p.strip()
            if p:
                cleaned_paths.append(p)
        
        return cleaned_paths  # BUG FIX: Return the cleaned paths
    
    def _get_passes_interactively(self):
        while True:
            try:
                passes_input = input("Number of overwrite passes (default is 3): ").strip()
                if not passes_input:
                    return 3
                passes = int(passes_input)
                if passes <= 0:
                    print("Number of passes must be positive. Please try again.")
                    continue
                return passes
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

    def run(self):
        args = self.parser.parse_args()

        # BUG FIX: Properly assign variables
        if args.paths:
            paths = args.paths 
        else: 
            paths = self.get_paths_interactively()  # Fixed: assign the return value
            if not paths:  # Exit if no paths provided
                return

        # BUG FIX: Properly assign passes variable
        if args.passes is not None:
            passes = args.passes  
        else:
            passes = self._get_passes_interactively()  # Fixed: assign the return value

        print(f"\nStarting secure erasure with {passes} passes...")
        
        # Securely erase each path
        success_count = 0
        total_count = len(paths)
        
        for path in paths:
            if self.overwriter.process_path(path, passes):
                success_count += 1
        
        print(f"\nOperation completed: {success_count}/{total_count} paths processed successfully.")


