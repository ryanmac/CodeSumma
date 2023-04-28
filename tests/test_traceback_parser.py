# tests/test_traceback_parser.py
from src.traceback_parser import (
    get_function_context,
    get_line_context,
    parse_traceback,
    format_parsed_traceback,
)
from src.utils import FunctionInfo


def test_get_function_context():
    file_path = 'tests/test_files/test_file.py'
    line_number = 5
    expected = {
        'info': FunctionInfo('divide',
                             [
                                {'name': 'a', 'type': 'Any'},
                                {'name': 'b', 'type': 'Any'}
                             ]),
        'summary': 'divide(a, b)',
        'body': ['def divide(a, b):']
    }
    actual = get_function_context(file_path, line_number)
    assert actual == expected


def test_get_line_context():
    file_path = 'tests/test_files/test_file.py'
    line_number = 5
    context = 1
    expected = [
        (4, ''),
        (5, 'def divide(a, b):'),
        (6, '    return a / b'),
    ]
    actual = get_line_context(file_path, line_number, context)
    assert actual == expected


def test_parse_traceback():

    tb_str = """Traceback (most recent call last):
File "tests/test_files/test_file.py", line 5, in divide
return a / b
        ~~^~~
ZeroDivisionError: division by zero
"""
    expected = [
        {
            "file_path": "tests/test_files/test_file.py",
            "line_number": 5,
            "function_context": {
                'info': FunctionInfo('divide',
                                     [
                                        {'name': 'a', 'type': 'Any'},
                                        {'name': 'b', 'type': 'Any'}
                                     ]
                                     ),
                'summary': 'divide(a, b)',
                'body': ['def divide(a, b):']
            },
            "line_context": [
                (2, "    return a + b"),
                (3, ""),
                (4, ""),
                (5, "def divide(a, b):"),
                (6, "    return a / b"),
            ]
        },
    ]
    actual = parse_traceback(tb_str)
    assert actual == expected


def test_format_parsed_traceback():
    parsed_traceback = [
        {
            "file_path": "tests/test_files/test_file.py",
            "line_number": 3,
            "function_context": None,
            "line_context": [
                (1, "def add(a, b):"),
                (2, "    return a + b"),
                (3, ""),
                (4, "def divide(a, b):"),
            ]
        },
        {
            "file_path": "tests/test_files/test_file.py",
            "line_number": 8,
            "function_context": {
                'info': FunctionInfo('divide',
                                     [
                                        {'name': 'a', 'type': 'Any'},
                                        {'name': 'b', 'type': 'Any'}
                                     ]
                                     ),
                'summary': 'divide(a, b)',
                'body': ['def divide(a, b):', '    return a / b']
            },
            "line_context": [
                (7, "def divide(a, b):"),
                (8, "    return a / b"),
            ]
        },
    ]
    expected = """File: tests/test_files/test_file.py
Line: 3

File: tests/test_files/test_file.py
Line: 8
Function: divide
Summary: divide(a, b)
def divide(a, b):
    return a / b
"""
    actual = format_parsed_traceback(parsed_traceback)
    assert actual.strip() == expected.strip()
