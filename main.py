import os
import argparse
import logging
from datetime import datetime

# mkdir os
if not os.path.exists("log"):
    os.mkdir("log")

# Getting time stamp
timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")

NOTICE_LEVEL = 25
logging.addLevelName(NOTICE_LEVEL, "NOTICE")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"log/code-counting-{timestamp}.log"),
    ],
)

# Create a StreamHandler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(NOTICE_LEVEL)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger().addHandler(console_handler)
logger = logging.getLogger(__name__)


def count_code_lines(repo_path, ignored_dirs=None, file_types=None):
    """
    Count the number of code lines in a repository, with options to ignore folders and filter by file extensions.
    :param repo_path: Repository path
    :param ignored_dirs: List of directory names to ignore
    :param file_types: List of file extensions to include (e.g., ['.py', '.cpp']); if None, include all
    :return: (total_lines, lines_per_extension)
    """
    total_lines = 0
    lines_per_extension = {}

    for root, dirs, files in os.walk(repo_path):
        # Remove directories to ignore
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext == "":
                logging.info(f"Ignoring dotfiles {file}")
                continue
            # If file_types is specified, only count those extensions
            if (not file_types) or (ext in file_types):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        num_lines = len(lines)
                        total_lines += num_lines
                        lines_per_extension[ext] = (
                            lines_per_extension.get(ext, 0) + num_lines
                        )
                        logging.info(f"📄 {file_path}: {num_lines} lines")
                except UnicodeDecodeError:
                    logging.warning(f"Skipping binary or non-UTF-8 file: {file_path}")
                except Exception as e:
                    logging.error(f"Error reading {file_path}: {e}")

    return total_lines, lines_per_extension


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Parser for code-line counting")

    parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="The path for the repo to be counted",
    )

    parser.add_argument(
        "--file_type",
        type=str,
        default=None,
        nargs="+",
        help="File types to be selected (e.g. .py .cpp .h)",
    )

    parser.add_argument(
        "--ignored_dir", type=str, nargs="+", default=None, help="Subdirs to be ignored"
    )

    args = parser.parse_args()

    # Prepare parameters
    file_types = args.file_type if args.file_type is not None else None
    repo_path = args.path
    ignored_dirs = (
        args.ignored_dir
        if args.ignored_dir is not None
        else [
            ".git",
            ".history",
            ".vscode",
            "build",
            "__pycache__",
            "log",
        ]
    )

    if not os.path.isdir(repo_path):
        logging.error("Invalid path!")
    else:
        total, per_ext = count_code_lines(repo_path, ignored_dirs, file_types)
        logging.log(NOTICE_LEVEL, f"Total lines of code: {total}")
        for ext, count in per_ext.items():
            logging.log(NOTICE_LEVEL, f"{ext}: {count}")
