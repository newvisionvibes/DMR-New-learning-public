import os

SEARCH_ROOT = "."  # change to your project root if needed
TARGET = "use_container_width=True"

def find_files_with_string(root_dir, target):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check only typical text/code files; remove this filter if you want all files
            if filename.endswith((".py", ".txt", ".md", ".log", ".cfg", ".ini")):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if target in line:
                                print(full_path)
                                # break after first hit in this file
                                break
                except (UnicodeDecodeError, PermissionError):
                    # Skip binary or unreadable files
                    continue

if __name__ == "__main__":
    find_files_with_string(SEARCH_ROOT, TARGET)
