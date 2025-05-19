from erasure.overwrite import Overwriter
import argparse


def run_cli():
   parser = argparse.ArgumentParser(description="Secure Erase Tool")
   parser.add_argument("paths", nargs="*", help="Files or folders to erase")
   parser.add_argument("--passes", type=int, default=None, help="Number of overwrite passes")
   args = parser.parse_args()


if not args.paths:
    print("\n[Interactive Mode]")
    print("No file paths provided. Let's collect them now.")
    raw_paths = input("Enter one or more file/folder paths (separated by commas): ").strip()
    paths = []
    for p in raw_paths.split(","):
       cleaned = p.strip()
       if cleaned:
          paths.append(cleaned)
else:
    paths = args.paths

if args.passes is None:
    try:
        passes = int(input("Number of overwrite passes (default is 3): ").strip() or "3")
    except ValueError:
        print("Invalid input. Using default (3) passes.")
        passes = 3
else:
    passes = args.passes

overwriter = Overwriter()

for path in paths:
    overwriter.process_path(path, passes=passes)
