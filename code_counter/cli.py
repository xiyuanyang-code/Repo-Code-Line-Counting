import os
import logging
import argparse
import colorama
from colorama import Style, Fore
from .counter import count_code_lines, setup_logging, NOTICE_LEVEL
from datetime import datetime

# Get logger for this module. Note: setup_logging configures the root logger,
# but it's good practice to get a named logger for each module.
logger = logging.getLogger(__name__)


def main():
    """
    Main function to parse arguments and run the code counting.
    """
    parser = argparse.ArgumentParser(
        description="Count the number of code lines in a repository."
    )

    parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="The path to the repository to be counted. Defaults to the current working directory.",
    )

    parser.add_argument(
        "--file_type",
        type=str,
        default=None,
        nargs="+",
        help="List of file extensions to include (e.g., .py .cpp .h). If None, all file types are counted.",
    )

    parser.add_argument(
        "--ignored_dir",
        type=str,
        default=[
            ".git",
            ".history",
            ".vscode",
            "build",
            "__pycache__",
            "log",
        ],  # Set default ignored directories
        nargs="+",
        help="List of subdirectory names to ignore. Defaults to common ignore directories.",
    )

    parser.add_argument(
        "--log_level",
        type=str,
        default="NOTICE",
        choices=[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "NOTICE",
        ],  # Add choices for validation
        help="Set the logging level for console output (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTICE). Defaults to NOTICE.",
    )

    args = parser.parse_args()

    # Setup logging based on parsed arguments
    timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, f"code-counting-{timestamp}.log")

    # Convert log level string to numeric level
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        # Handle custom NOTICE_LEVEL if needed, or rely on setup_logging
        if args.log_level.upper() == "NOTICE":
            numeric_level = NOTICE_LEVEL
        else:
            print(f"Invalid log level: {args.log_level}. Using NOTICE.")
            numeric_level = NOTICE_LEVEL  # Fallback

    setup_logging(log_file_path, console_level=numeric_level)

    try:
        # Call the counting function with parsed arguments
        total, per_ext = count_code_lines(args.path, args.ignored_dir, args.file_type)

        logger.log(NOTICE_LEVEL, f"--- Code Counting Report for: {args.path} ---")
        logger.log(NOTICE_LEVEL, f"Total lines of code: {total}")
        logger.log(NOTICE_LEVEL, "Lines per extension:")
        # Sort by lines in descending order for better readability
        for ext, count in sorted(
            per_ext.items(), key=lambda item: item[1], reverse=True
        ):
            logger.log(NOTICE_LEVEL, f"  {ext}: {count}")
        logger.log(NOTICE_LEVEL, "-------------------------------------")
        print(total)
        print(Fore.GREEN + str(per_ext) + Style.RESET_ALL)

    except ValueError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
