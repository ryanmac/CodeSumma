# tests/test_file_processing.py
from src.file_processing import (
    get_file_hierarchy,
    format_file_hierarchy,
    get_ignore_patterns,
    check_ignore_patterns,
)


def test_get_file_hierarchy():
    path = 'tests/test_files/'
    ignore_patterns = get_ignore_patterns(path)
    expected = ['/', '    test_file.py', '    test_file2.py', '    traceback.txt']
    actual = get_file_hierarchy(path, ignore_patterns=ignore_patterns)
    assert actual == expected


def test_format_file_hierarchy():
    path = 'tests/test_files/'
    ignore_patterns = get_ignore_patterns(path)
    expected = "/\n    test_file.py\n    test_file2.py\n    traceback.txt"
    actual = format_file_hierarchy(path, ignore_patterns)
    print(f"Actual: {actual}\nExpected: {expected}")
    assert actual == expected


def test_get_ignore_patterns():
    path = 'tests/test_files/'
    expected = [
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
    actual = get_ignore_patterns(path)
    assert set(actual) == set(expected)


def test_check_ignore_patterns():
    path = 'tests/test_files/.gitignore'
    ignore_patterns = get_ignore_patterns(path)
    assert check_ignore_patterns(path, ignore_patterns)

    path = 'tests/test_files/test_file.py'
    assert not check_ignore_patterns(path, ignore_patterns)
