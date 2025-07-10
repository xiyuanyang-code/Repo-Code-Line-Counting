import os
import logging
import pathspec



NOTICE_LEVEL = 25
if not hasattr(logging, "NOTICE"):
    logging.addLevelName(NOTICE_LEVEL, "NOTICE")
    logging.NOTICE = NOTICE_LEVEL  # type: ignore

# Base logger for the module
logger = logging.getLogger(__name__)


def setup_logging(
    log_file_path=None, console_level=NOTICE_LEVEL, file_level=logging.DEBUG
):
    """
    Configures logging for the application.
    :param log_file_path: Optional path for the log file. If None, no file handler is added.
    :param console_level: Logging level for console output.
    :param file_level: Logging level for file output.
    """
    # Ensure handlers are not duplicated if setup_logging is called multiple times
    for handler in logger.handlers[:]:  # Iterate over a slice to allow modification
        logger.removeHandler(handler)

    logger.setLevel(min(console_level, file_level) if log_file_path else console_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def load_gitignore_patterns(repo_path):
    """
    Load .gitignore patterns using pathspec, if available.
    Returns a PathSpec object or None if .gitignore does not exist or pathspec is not installed.
    """
    gitignore_path = os.path.join(repo_path, ".gitignore")
    if not os.path.isfile(gitignore_path) or pathspec is None:
        return None
    with open(gitignore_path, "r", encoding="utf-8") as f:
        patterns = f.read().splitlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def is_ignored_by_gitignore(path, repo_path, gitignore_spec: pathspec.PathSpec):
    """
    Check if a path is ignored by .gitignore.
    """
    if gitignore_spec is None:
        return False
    # Make path relative to repo root
    rel_path = os.path.relpath(path, repo_path)
    return gitignore_spec.match_file(rel_path)


def count_code_lines(repo_path, ignored_dirs=None, file_types=None):
    """
    Count the number of code lines in a repository, with options to ignore folders and filter by file extensions.
    Also ignores files/directories specified in .gitignore if pathspec is installed.
    :param repo_path: Repository path
    :param ignored_dirs: List of directory names to ignore
    :param file_types: List of file extensions to include (e.g., ['.py', '.cpp']); if None, include all
    :return: (total_lines, lines_per_extension)
    """
    total_lines = 0
    lines_per_extension = {}
    default_ignored_dirs = [
        ".git",
        ".history",
        ".vscode",
        "build",
        "__pycache__",
        "log",
        "venv",
        ".DS_Store",
        "node_modules",
    ]

    # Default ignored directories if not provided
    if ignored_dirs is None:
        ignored_dirs = default_ignored_dirs
    else:
        ignored_dirs = list(set(default_ignored_dirs + ignored_dirs))

    # Load .gitignore patterns if possible
    gitignore_spec = load_gitignore_patterns(repo_path)

    if not os.path.isdir(repo_path):
        logger.error(f"Invalid path: {repo_path}")
        raise ValueError(
            f"Repository path does not exist or is not a directory: {repo_path}"
        )

    for root, dirs, files in os.walk(repo_path):
        # Remove directories to ignore in place
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        # Remove dirs ignored by .gitignore
        if gitignore_spec is not None:
            dirs[:] = [
                d
                for d in dirs
                if not is_ignored_by_gitignore(
                    os.path.join(root, d), repo_path, gitignore_spec
                )
            ]

        for file in files:
            file_path = os.path.join(root, file)
            file_name, ext = os.path.splitext(file)
            if ext == "":
                logger.debug(
                    f"Ignoring file without extension (likely a dotfile or binary): {file}"
                )
                continue

            # Ignore files matched by .gitignore
            if gitignore_spec is not None and is_ignored_by_gitignore(
                file_path, repo_path, gitignore_spec
            ):
                logger.debug(f"Skipping file ignored by .gitignore: {file_path}")
                continue

            # If file_types is specified, only count those extensions
            if (not file_types) or (
                ext.lower() in [ft.lower() for ft in file_types]
            ):  # Convert to lower for case-insensitivity
                try:
                    # Check if it's a symbolic link and skip to avoid infinite loops or errors
                    if os.path.islink(file_path):
                        logger.debug(f"Skipping symbolic link: {file_path}")
                        continue

                    # Attempt to open and read as text; will fail for true binaries
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        num_lines = len(lines)
                        total_lines += num_lines
                        lines_per_extension[ext] = (
                            lines_per_extension.get(ext, 0) + num_lines
                        )
                        logger.debug(f"📄 {file_path}: {num_lines} lines")
                except UnicodeDecodeError:
                    logger.warning(f"Skipping binary or non-UTF-8 file: {file_path}")
                except Exception as e:
                    logger.error(f"Error reading {file_path}: {e}")

    return total_lines, lines_per_extension
