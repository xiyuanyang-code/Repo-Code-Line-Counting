import os
import logging
import fire
from .counter import count_code_lines, setup_logging, NOTICE_LEVEL
from datetime import datetime

class CodeCounterCLI:
    def __init__(self):
        # Initial setup for logging, but allows for dynamic changes via CLI
        timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
        log_dir = "log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir) # Use makedirs to create intermediate directories if needed
        self.log_file_path = os.path.join(log_dir, f"code-counting-{timestamp}.log")
        setup_logging(self.log_file_path) # Setup logging with a file handler by default

    def count(self,
              path: str = os.getcwd(),
              file_type: list[str] = None, # type: ignore
              ignored_dir: list[str] = None, # type: ignore
              log_level: str = "NOTICE"):
        """
        Count the number of code lines in a repository.

        Args:
            path (str): The path to the repository to be counted. Defaults to the current working directory.
            file_type (list[str]): List of file extensions to include (e.g., .py .cpp .h). If None, all file types are counted.
            ignored_dir (list[str]): List of subdirectory names to ignore. Defaults to common ignore directories.
            log_level (str): Set the logging level for console output (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTICE).
                             Defaults to NOTICE.
        """
        # Dynamically set console log level based on user input
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            try:
                numeric_level = int(log_level)
            except ValueError:
                print(f"Invalid log level: {log_level}. Using NOTICE.")
                numeric_level = NOTICE_LEVEL
        
        setup_logging(self.log_file_path, console_level=numeric_level)

        logger = logging.getLogger(__name__) # Get logger instance after setup

        try:
            total, per_ext = count_code_lines(path, ignored_dir, file_type)
            logger.log(NOTICE_LEVEL, f"--- Code Counting Report for: {path} ---")
            logger.log(NOTICE_LEVEL, f"Total lines of code: {total}")
            logger.log(NOTICE_LEVEL, "Lines per extension:")
            # Sort by lines in descending order for better readability
            for ext, count in sorted(per_ext.items(), key=lambda item: item[1], reverse=True):
                logger.log(NOTICE_LEVEL, f"  {ext}: {count}")
            logger.log(NOTICE_LEVEL, "-------------------------------------")

        except ValueError as e:
            logger.error(f"Error: {e}")
        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")

def main():
    fire.Fire(CodeCounterCLI)

if __name__ == '__main__':
    main()
