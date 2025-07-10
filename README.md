# Code Line Counting Tool

This tool counts the number of code lines in a repository, with options to ignore specific folders and filter by file extensions. It logs detailed results to both the console and a log file.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/xiyuanyang-code/Repo-Code-Line-Counting.git
    cd Repo-Code-Line-Counting
    ```
2.  Install the package (preferably in a virtual environment):
    ```bash
    pip install .
    ```
    For development, you can install in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

### Command Line Interface

After installation, you can use the `count-code` command directly in your terminal.

```bash
count-code [OPTIONS]
```

**Options:**

*   `--path PATH`: The path to the repository to be counted. Defaults to the current working directory (`.`).
*   `--file_type FILE_TYPE [FILE_TYPE ...]`: List of file extensions to include (e.g., `.py .cpp .h`). If not provided, all file types are counted.
*   `--ignored_dir IGNORED_DIR [IGNORED_DIR ...]`: List of subdirectory names to ignore. Defaults to common ignore directories (`.git`, `.history`, `.vscode`, `build`, `__pycache__`, `log`).
*   `--log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL,NOTICE}`: Set the logging level for console output. Defaults to `NOTICE`.

**Examples:**

Count lines in the current directory (using default ignored directories and counting all file types):

```bash
count-code
```

Count only `.cpp` and `.hpp` files in a specific repository:

```bash
count-code --path /home/xiyuanyang/ACM_course_DS/Data_structure --file_type ".cpp" ".hpp"
```

Count lines ignoring the `docs` and `tests` directories:

```bash
count-code --ignored_dir "docs" "tests"
```

Run with DEBUG logging level:

```bash
count-code --log_level DEBUG
```

### As a Python Module

You can also import and use the `count_code_lines` function directly in your Python code.

```python
import os
from code_counter.counter import count_code_lines, setup_logging, NOTICE_LEVEL
import logging
from datetime import datetime

# Setup logging (optional, but recommended for consistent output)
timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_path = os.path.join(log_dir, f"code-counting-{timestamp}.log")
setup_logging(log_file_path, console_level=NOTICE_LEVEL)
logger = logging.getLogger(__name__)


# Example usage:
repo_path = "/home/xiyuanyang/Hodgepodge/repo_counting"
ignored_dirs = [".git", "log"]
file_types = [".py", ".md"]

total_lines, lines_per_extension = count_code_lines(repo_path, ignored_dirs, file_types)

logger.log(NOTICE_LEVEL, f"--- Module Usage Report for: {repo_path} ---")
logger.log(NOTICE_LEVEL, f"Total lines counted: {total_lines}")
logger.log(NOTICE_LEVEL, "Lines per extension:")
for ext, count in sorted(lines_per_extension.items(), key=lambda item: item[1], reverse=True):
    logger.log(NOTICE_LEVEL, f"  {ext}: {count}")
logger.log(NOTICE_LEVEL, "-------------------------------------")

# You can also access the raw results:
print(f"Raw total lines: {total_lines}")
print(f"Raw lines per extension: {lines_per_extension}")
```

## Log Output

Detailed logs, including file-by-file line counts and any errors encountered, are saved to a file in the `log/` directory (e.g., `log/code-counting-YYYYMMDD_HH-MM-SS.log`). Summary results are also printed to the console based on the specified log level.

## Todo

*   Add support for file matching using regular expressions.
