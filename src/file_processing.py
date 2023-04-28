# src/file_processing.py
import os
import tempfile


def get_file_hierarchy(path, prefix='', ignore_patterns=None):
    """
    Get a list of files and directories in a directory, recursively.

    Args:
        path (str): The path to the directory.
        prefix (str): The prefix to add to each file and directory.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        list: A list of files and directories in the directory.
    """

    if ignore_patterns is None:
        raise ValueError("ignore_patterns must be provided")
    output = []

    if os.path.isfile(path):

        if not check_ignore_patterns(path, ignore_patterns):
            output.append(f"{prefix}{os.path.basename(path)}")

    elif os.path.isdir(path):
        dirname = os.path.basename(path)

        if not check_ignore_patterns(dirname, ignore_patterns):
            output.append(f"{prefix}{dirname}/")
            prefix += '    '

            for entry in sorted(os.listdir(path)):
                entry_path = os.path.join(path, entry)
                output += get_file_hierarchy(entry_path, prefix, ignore_patterns)

    return output


def format_file_hierarchy(path, ignore_patterns):
    """
    Format the output of get_file_hierarchy().

    Args:
        path (str): The path to the directory.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        str: The formatted output.
    """

    prefix = ''
    file_hierarchy = get_file_hierarchy(path, prefix, ignore_patterns)

    # Replace the temporary directory with './'
    path_absolute = os.path.abspath(path)
    if os.path.commonpath(
                [path_absolute, tempfile.gettempdir()]
            ) == tempfile.gettempdir():
        file_hierarchy[0] = './'

    return '\n'.join(file_hierarchy)


def get_ignore_patterns(input_path, ignore_patterns=None):
    """
    Get a list of patterns to ignore.

    Args:
        input_path (str): The path to the input file or directory.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        list: A list of patterns to ignore.
    """

    default_ignore_patterns = [
        '__pycache__',
        '.DS_Store',
        'egg-info',
        '.env',
        '.git',
        '.ipynb_checkpoints',
        '.pkl',
        '.pyc',
        '.pytest_cache',
        '.vscode',
        'dist',
        'LICENSE',
        'venv',
    ]

    git_ignore_patterns = []
    if os.path.isdir(input_path):
        gitignore_path = os.path.join(input_path, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_contents = f.read()
            git_ignore_patterns += gitignore_contents.splitlines()

    if ignore_patterns is None:
        ignore_patterns = []
    elif isinstance(ignore_patterns, str):
        ignore_patterns = ignore_patterns.split(',')
    elif len(ignore_patterns) == 1 and isinstance(ignore_patterns[0], str):
        ignore_patterns = ignore_patterns[0].split(',')

    ignore_patterns += default_ignore_patterns
    ignore_patterns += git_ignore_patterns
    return ignore_patterns


def check_ignore_patterns(path, ignore_patterns):
    """
    Check if a path matches any of the ignore patterns.

    Args:
        path (str): The path to the file or directory.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        bool: True if the path matches any of the ignore patterns, False otherwise.
    """

    for pattern in ignore_patterns:
        if pattern.lower() in path.lower():
            return True
    return False


def get_all_code(dir_path, ignore_patterns):
    """
    Get all code in a directory, recursively.

    Args:
        dir_path (str): The path to the directory.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        dict: A dictionary of file paths and code.
    """

    summary = {}
    for root, dirs, files in os.walk(dir_path):

        for dir in dirs:
            if check_ignore_patterns(dir, ignore_patterns):
                dirs.remove(dir)

        for file in files:

            file_path = os.path.join(root, file)

            if check_ignore_patterns(file_path, ignore_patterns):
                continue

            code = []
            with open(file_path, 'r') as f:
                code.append(f.read())
            summary[file_path] = code

    return summary
