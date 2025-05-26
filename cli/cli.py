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
        paths = raw_paths.split(",")
        cleaned_paths = []
        for p in paths:
            p = p.strip()
            if p:
                cleaned_paths.append(p)
        return cleaned_paths
    
   
    def _get_passes_interactively(self):
        try:
            return int(input("Number of overwrite passes (default is 3): ").strip() or "3")
        except ValueError:
            print("Invalid input. Using default (3) passes.")
            return 3

    def run(self):
        args = self.parser.parse_args()

        # Get file/folder paths
        if(args.paths):
            paths = args.paths 
        else: 
            self.get_paths_interactively()

        # Get overwrite passes
        if(args.passes):
            passes = args.passes  
        else:
            self._get_passes_interactively()

        # Securely erase each path
        for path in paths:
            self.overwriter.process_path(path, passes)
   
    # def run_cli():
    #     parser = argparse.ArgumentParser(description="Secure Erase Tool")
    #     parser.add_argument("paths", nargs="*", help="Files or folders to erase")
    #     parser.add_argument("--passes", type=int, default=None, help="Number of overwrite passes")
    #     args = parser.parse_args()


    #     if not args.paths:
    #         print("\n[Interactive Mode]")
    #         print("No file path provided. Let's collect them now.")
    #         raw_paths = input("Enter one or paths (separated by commas): ").strip()
    #         paths = []
    #         for p in raw_paths.split(","):
    #             cleaned = p.strip()
    #             if cleaned:
    #                 paths.append(cleaned)
    #     else:
    #         paths = args.paths

    #     if args.passes is None:
    #         try:
    #             passes = int(input("Number of overwrite passes (default is 3): ").strip() or "3")
    #         except ValueError:
    #             print("Invalid input. Using default (3) passes.")
    #             passes = 3
    #     else:
    #         passes = args.passes

    #     overwriter = Overwriter(Logger())

    #     for path in paths:
    #         overwriter.process_path(path, passes)
