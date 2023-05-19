# src/utils.py
import argparse
import ast


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate code summary for Python files and directories.'
    )
    parser.add_argument(
        'input_path',
        type=str,
        default='.',
        help='Path to a Python file or a directory'
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Write out all code'
    )
    parser.add_argument(
        '-cp', '--copy',
        action='store_true',
        help='Copy output to clipboard - requires pyperclip)'
    )
    parser.add_argument(
        '-i', '--ignore',
        metavar='pattern',
        nargs='+',
        help='Ignore patterns (e.g. "*.pyc")'
    )
    parser.add_argument(
        '-m', '--manual',
        action='store_true',
        help='Prompt user for all inputs. Helpful for pasting traceback.'
    )
    parser.add_argument(
        '-o', '--max-tokens-out',
        type=int,
        default=4096,
        help='Maximum tokens for output summary'
    )
    parser.add_argument(
        '-pf', '--print-full',
        metavar='pattern',
        nargs='+',
        help='Print full file content for files matching the pattern (e.g. "test_")'
    )
    parser.add_argument(
        '-po', '--print-only',
        metavar='pattern',
        nargs='+',
        help='Print full file content only for files matching the pattern (e.g. "test_")'
    )
    parser.add_argument(
        '-t', '--traceback',
        nargs='?',
        const=True,
        metavar='traceback_text',
        help='Provide traceback text for context or leave it empty to read from stdin'
    )

    return parser.parse_args()


def is_github_url(url):
    """
    Check if a URL is a GitHub URL.

    Args:
        url (str): URL to check

    Returns:
        bool: True if the URL is a GitHub URL, False otherwise.
    """

    return url.startswith("https://github.com/") or url.startswith("git@github.com:")


class FunctionInfo:
    """
    A class to represent a function's name, arguments, and return type.
    """

    def __init__(self, name, args, return_type=None):
        self.name = name
        self.args = args
        self.return_type = return_type

    def __str__(self):
        args = ', '.join([arg['name'] for arg in self.args])
        return f"{self.name}({args})"

    def __eq__(self, other):
        return (
                self.name == other.name
                and self.args == other.args
                and self.return_type == other.return_type
                )


def get_function_info(func_def):
    """
    Get the name and arguments of a function.

    Args:
        func_def (ast.FunctionDef): The function definition.

    Returns:
        FunctionInfo: The function's name and arguments.
    """

    args = [{'name': arg.arg, 'type': 'Any'} for arg in func_def.args.args]
    return FunctionInfo(func_def.name, args)


def process_class(cls):
    """
    Get the methods of a class.

    Args:
        cls (ast.ClassDef): The class definition.

    Returns:
        list: A list of the class's methods.
    """

    methods = []

    for item in cls.body:
        if isinstance(item, ast.FunctionDef):
            methods.append(get_function_info(item))

    return methods
