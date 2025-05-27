# Code Line Counting Tool

This tool counts the number of code lines in a repository, with options to ignore specific folders and filter by file extensions. It logs detailed results to both the console and a log file.

## Usage

Run the script from the command line:

```bash
python main.py --path /home/xiyuanyang/ACM_course_DS/Data_structure --file_type ".cpp" ".hpp"
```

- `--path`: Path to the repository to be counted.

- `--file_type`: (Optional) List of file extensions to include (e.g., ".py" ".cpp" ".h"). If omitted, all file types are counted.

- `--ignored_dir`: (Optional) List of subdirectories to ignore.

## Log Output Example

```
2025-05-27 10:52:55,124 - NOTICE - Total lines of code: 12037
2025-05-27 10:52:55,124 - NOTICE - Lines per file extension:
2025-05-27 10:52:55,124 - NOTICE - .cpp: 8876
2025-05-27 10:52:55,125 - NOTICE - .hpp: 3161
```
All results are also saved to a log file in ~/.log/. 