# tests/test_summary.py
import ast
from src.summary import (
    generate_summary_from_python_file,
    summarize_directory,
    format_summary,
)
from src.utils import FunctionInfo, get_function_info


def test_generate_summary_from_python_file():
    # Test that generate_summary_from_python_file returns the correct functions
    # for a given file
    file_path = 'tests/test_files/test_file2.py'
    expected = [
        FunctionInfo('add',
                     [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        FunctionInfo('subtract',
                     [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        FunctionInfo('multiply',
                     [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        FunctionInfo('divide',
                     [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        FunctionInfo('modulus',
                     [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
    ]
    actual = generate_summary_from_python_file(file_path)
    assert actual == expected


def test_get_function_info():
    # Test that get_function_info returns the correct FunctionInfo object
    # for a given function definition
    func_def = ast.parse("""def add(a, b):
    return a + b
""").body[0]

    expected = FunctionInfo('add',
                            [
                                {'name': 'a', 'type': 'Any'},
                                {'name': 'b', 'type': 'Any'}
                            ])
    actual = get_function_info(func_def)
    assert actual == expected


def test_summarize_directory():
    # Test that summarize_directory returns the correct summary for a given directory
    dir_path = 'tests/test_files'
    expected = {
        'tests/test_files/traceback.txt': [],
        'tests/test_files/test_file.py': [
            FunctionInfo('add',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('divide',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        ],
        'tests/test_files/test_file2.py': [
            FunctionInfo('add',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('subtract',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('multiply',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('divide',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('modulus',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        ],
    }
    actual = summarize_directory(dir_path, ignore_patterns=['pycache'])

    # Loop through the keys in expected and assert that the values are equal
    for key in expected.keys():
        print(f"Testing {key}\nActual: {actual[key]}\nExpected: {expected[key]}")
        assert actual[key] == expected[key]


def test_format_summary():
    # Test that format_summary returns the correct string for a given summary
    summary = {
        'tests/test_files/test_file.py': [
            FunctionInfo('add',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('divide',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        ],
        'tests/test_files/test_file2.py': [
            FunctionInfo('add',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('subtract',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('multiply',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('divide',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
            FunctionInfo('modulus',
                         [{'name': 'a', 'type': 'Any'}, {'name': 'b', 'type': 'Any'}]),
        ],
    }

    expected = """File: tests/test_files/test_file.py
```
add(a, b)
divide(a, b)
```

File: tests/test_files/test_file2.py
```
add(a, b)
subtract(a, b)
multiply(a, b)
divide(a, b)
modulus(a, b)
```
"""
    actual = format_summary(summary)
    assert actual == expected
