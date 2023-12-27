# src/traceback_parser.py
import ast
import re
from typing import List, Dict, Any
from utils import get_function_info


def get_function_context(file_path, line_number):
    """
    Get the function context for the function that contains the given line number.

    Args:
        file_path (str): The path to the file to parse.
        line_number (int): The line number to get the function context for.

    Returns:
        dict: A dictionary containing the function context.
    """

    with open(file_path, 'r') as f:
        file_contents = f.read()

    module = ast.parse(file_contents)
    func_def = None

    for item in module.body:
        if (
            isinstance(item, ast.FunctionDef)
            and item.lineno <= line_number <= item.end_lineno
        ):
            func_def = item
            break

    if func_def is None:
        return None

    function_info = get_function_info(func_def)
    function_body = file_contents.splitlines()[
        func_def.lineno - 1:func_def.end_lineno - 1
        ]
    function_summary = str(function_info)

    return {
        'info': function_info,
        'summary': function_summary,
        'body': function_body
    }


def get_line_context(file_path, line_number, context=3):
    """
    Get the lines of code surrounding the given line number in the given file.

    Args:
        file_path (str): The path to the file to parse.
        line_number (int): The line number to get the context for.
        context (int): The number of lines of context to include on either side of the
            given line number.

    Returns:
        list: A list of tuples containing the line number and line contents for each
            line of context.
    """

    with open(file_path, 'r') as f:
        file_contents = f.readlines()

    start = max(0, line_number - context - 1)
    end = min(len(file_contents), line_number + context)
    lines = file_contents[start:end]

    return [(idx + 1, line.rstrip()) for idx, line in enumerate(lines, start=start)]


def parse_traceback(tb_str: str) -> List[Dict[str, Any]]:
    """
    Parse a traceback string into a list of dictionaries containing
        information about each frame.

    Args:
        tb_str (str): The traceback string to parse.

    Returns:
        list: A list of dictionaries containing information about each frame.
    """

    # Split the traceback string into lines
    tb_lines = tb_str.splitlines()

    # Extract the traceback frames using a regular expression
    tb_pattern = re.compile(
        r'^\s*File "([^"]+)", line (\d+)(?:, in (\w+))?.*$',
    )
    tb_frames = [match.groups() for match in map(tb_pattern.match, tb_lines) if match]

    parsed_traceback = []

    for file_path, line_number_str, _ in tb_frames:
        line_number = int(line_number_str)

        # Get function context
        function_context = get_function_context(file_path, line_number)

        # Get line context
        line_context = get_line_context(file_path, line_number)

        parsed_frame = {
            "file_path": file_path,
            "line_number": line_number,
            "function_context": function_context,
            "line_context": line_context
        }

        parsed_traceback.append(parsed_frame)

    return parsed_traceback


def format_parsed_traceback(parsed_traceback):
    """
    Format a parsed traceback into a string.

    Args:
        parsed_traceback (list): A list of dictionaries containing information
            about each frame.

    Returns:
        str: A string containing the formatted traceback.
    """

    formatted_traceback = []
    for frame in parsed_traceback:
        file_path = frame["file_path"]
        line_number = frame["line_number"]
        function_context = frame["function_context"]
        # line_context = frame["line_context"]

        formatted_frame = [f"File: {file_path}", f"Line: {line_number}"]

        if function_context:
            formatted_frame.append(f"Function: {function_context['info'].name}")
            formatted_frame.append(f"Summary: {function_context['summary']}")
            # formatted_frame.append("Function Body:")
            formatted_frame.extend(function_context['body'])

        # formatted_frame.append("Context:")
        # formatted_frame.extend([f"{idx}: {line}" for idx, line in function_context])

        formatted_traceback.append("\n".join(formatted_frame))

    return "\n\n".join(formatted_traceback)
