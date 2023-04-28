# src/summary.py
import ast
import os
import sys
import shutil
import fnmatch
from git import Repo
import tempfile
from .file_processing import check_ignore_patterns
from .openai_api import (
    call_openai_api,
    OPENAI_API_KEY,
    estimate_tokens,
    trim_string_to_token_limit,
)
from .file_processing import (
    format_file_hierarchy,
    get_ignore_patterns,
    get_all_code,
)
from .traceback_parser import (
    parse_traceback,
    format_parsed_traceback,
)
from .utils import (
    is_github_url,
    get_function_info,
)


def run_summary(args):

    input_path = args.input_path
    ignore_patterns = get_ignore_patterns(input_path, args.ignore)

    if is_github_url(input_path):
        print(f"Cloning {input_path}...")
        tmpdir = tempfile.mkdtemp()
        Repo.clone_from(input_path, tmpdir)
        print(f"Cloned to {tmpdir}")
        input_path = tmpdir

    print_full_patterns = args.print_full or []

    if isinstance(print_full_patterns, list) and len(print_full_patterns) == 1:
        print_full_patterns = print_full_patterns[0].split(',')

    if args.all:
        summary = get_all_code(input_path, ignore_patterns)
    elif os.path.isfile(input_path) and input_path.endswith('.py'):
        if any(fnmatch.fnmatch(input_path, pattern) for pattern in print_full_patterns):
            with open(input_path, 'r') as f:
                summary = {input_path: f.read()}
        else:
            summary = {input_path: generate_summary_from_python_file(input_path)}
    elif os.path.isdir(input_path):
        summary = summarize_directory(input_path, ignore_patterns, print_full_patterns)
    else:
        print("Invalid input. Please provide a path to a Python file or a directory.")
        sys.exit(1)

    summary_blocks = {
        "file_hierarchy": format_file_hierarchy(input_path, ignore_patterns),
        "file_summary": format_summary(summary),
        "traceback": args.traceback,
        "traceback_context": None,
    }

    if is_github_url(args.input_path):
        file_summary = summary_blocks["file_summary"].replace(tmpdir, "")
        summary_blocks["file_summary"] = file_summary
        # Delete the temporary directory
        shutil.rmtree(tmpdir)

    if not summary_blocks["file_summary"].strip():
        print("No code summary found.")
        sys.exit(0)

    if args.traceback is not None:

        if args.traceback is True:
            print("Paste Traceback:")
            traceback_lines = []
            while True:
                try:
                    line = input()
                    traceback_lines.append(line)
                except EOFError:
                    break
            traceback_str = "\n".join(traceback_lines)
        else:
            traceback_str = args.traceback

        summary_blocks["traceback"] = traceback_str

        parsed_traceback = parse_traceback(traceback_str)
        formatted_traceback = format_parsed_traceback(parsed_traceback)
        summary_blocks["traceback_context"] = formatted_traceback

    if not args.all:
        summary_blocks = summarize_blocks(summary_blocks, args.max_tokens_out)

    formatted_summary = f"""Context:

Directory Structure:
```
{summary_blocks['file_hierarchy']}
```

File Summary:
{summary_blocks['file_summary']}
"""

    if args.traceback is not None:
        formatted_summary += f"""
Traceback:
```
{summary_blocks['traceback']}
```

Traceback Context:
```
{summary_blocks['traceback_context']}
```

Resolve this error.
"""

    # Get some stats about the summary
    num_tokens = estimate_tokens(formatted_summary)

    return formatted_summary, num_tokens


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


def generate_summary_from_python_file(file_path):
    """
    Generate a summary of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        list: A list of the file's functions and classes.
    """

    if not file_path.endswith('.py'):
        return []

    with open(file_path, 'r') as f:
        file_contents = f.read()

    module = ast.parse(file_contents)
    summary_items = []

    for item in module.body:
        if isinstance(item, ast.FunctionDef):
            summary_items.append(get_function_info(item))
        elif isinstance(item, ast.ClassDef):
            summary_items.append(f"Class: {item.name}")
            class_methods = process_class(item)
            summary_items.extend(class_methods)

    return summary_items


def summarize_directory(dir_path, ignore_patterns=None, print_full_patterns=None):
    """
    Generate a summary of a directory.

    Args:
        dir_path (str): The path to the directory.
        ignore_patterns (list, optional): A list of patterns to ignore.
            Defaults to None.
        print_full_patterns (list, optional): A list of patterns to print the full
            file instead of summarizing. Defaults to None.

    Returns:
        dict: A dictionary of the directory's files and their summaries.
    """

    if ignore_patterns is None:
        ignore_patterns = []
    if print_full_patterns is None:
        print_full_patterns = []

    summary = {}
    for root, dirs, files in os.walk(dir_path):

        dirs[:] = [d for d in dirs if not check_ignore_patterns(d, ignore_patterns)]

        for file in files:
            if (
                not check_ignore_patterns(file, ignore_patterns)
                and not check_ignore_patterns(root, ignore_patterns)
            ):
                file_path = os.path.join(root, file)

                # print_full_patterns is a list of strings. ex: ['init']
                # If any of the patterns are found in the file name string,
                # then print the full file instead of summarizing
                if any(
                        [fnmatch.fnmatch(file, f"*{pattern}*")
                            for pattern in print_full_patterns]
                        ) or any(
                        [fnmatch.fnmatch(file_path, f"*{pattern}*")
                            for pattern in print_full_patterns]
                        ):
                    print(f"Printing full file: {file_path}, Matching pattern: {print_full_patterns}")
                    with open(file_path, 'r') as f:
                        summary[file_path] = f.read()
                else:
                    if file_path.endswith('.py'):
                        functions = generate_summary_from_python_file(file_path)
                        summary[file_path] = functions
                    elif file_path.endswith('.ipynb'):
                        with open(file_path, 'r') as f:
                            code = f.read()
                        # If the code is too long, trim it to the token limit
                        code = trim_string_to_token_limit(code, 2000)
                        prompt = f"Summarize the following code:\n```\n{code}\n```"
                        summary[file_path] = call_openai_api(prompt, 500)
                    elif file_path.endswith('.md'):
                        with open(file_path, 'r') as f:
                            code = f.read()
                        # If the code is too long, trim it to the token limit
                        code = trim_string_to_token_limit(code, 2000)
                        prompt = f"Summarize the following:\n```\n{code}\n```"
                        summary[file_path] = call_openai_api(prompt, 500)
                    elif file_path.endswith('.sh'):
                        with open(file_path, 'r') as f:
                            code = f.read()
                        # If the code is too long, trim it to the token limit
                        code = trim_string_to_token_limit(code, 500)
                        prompt = f"""Summarize the following code:
```
{code}
```
Summarize any arguments, flags, functions, or options.
"""
                        summary[file_path] = call_openai_api(prompt, 2000)
                    elif file_path.endswith('.txt'):
                        summary[file_path] = []
                    else:

                        try:
                            with open(file_path, 'r') as f:
                                code = f.read()

                            code = trim_string_to_token_limit(code, 2000)
                            prompt = f"""Summarize the following code:
```
{code}
```
"""
                            summary[file_path] = call_openai_api(prompt, 200)

                        except UnicodeDecodeError:
                            summary[file_path] = []

    return summary


def summarize_blocks(summary_blocks, max_tokens_out=4096):
    """
    Summarize a list of blocks.

    Args:
        summary_blocks (list): A list of blocks to summarize.
            summary_blocks = {
                'file_hierarchy': file_hierarchy,
                'file_summary': file_summary,
                'traceback': traceback,
                'traceback_context': traceback_context
            }
        max_tokens_out (int, optional): The maximum number of tokens to output.
            Defaults to 4096.

    Returns:
        str: The summarized blocks.
    """

    traceback = (summary_blocks["traceback"]
                 if summary_blocks["traceback"] is not None
                 else "")
    traceback_context = (summary_blocks["traceback_context"]
                         if summary_blocks["traceback_context"] is not None
                         else "")

    remaining_tokens = max_tokens_out - estimate_tokens(traceback + traceback_context)

    if remaining_tokens <= 0:
        reduced_summary_blocks = {
            "file_hierarchy": "",
            "file_summary": "",
            "traceback": summary_blocks['traceback'],
            "traceback_context": trim_string_to_token_limit(
                summary_blocks['traceback_context'],
                (max_tokens_out - estimate_tokens(summary_blocks['traceback']))
            ),
        }
        return reduced_summary_blocks

    file_hierarchy = summary_blocks["file_hierarchy"]
    file_summary = summary_blocks["file_summary"]

    total_file_tokens = estimate_tokens(file_hierarchy) + estimate_tokens(file_summary)
    if total_file_tokens <= remaining_tokens:
        reduced_summary_blocks = {
            "file_hierarchy": file_hierarchy,
            "file_summary": file_summary,
            "traceback": summary_blocks['traceback'],
            "traceback_context": summary_blocks['traceback_context'],
        }
        return reduced_summary_blocks

    reduced_file_summary = summarize_file_summaries(
        file_summary,
        (remaining_tokens - estimate_tokens(file_hierarchy))
        )

    token_estimate = (
        estimate_tokens(file_hierarchy) + estimate_tokens(reduced_file_summary)
    )
    if (token_estimate <= remaining_tokens):
        reduced_summary_blocks = {
            "file_hierarchy": file_hierarchy,
            "file_summary": reduced_file_summary,
            "traceback": summary_blocks['traceback'],
            "traceback_context": summary_blocks['traceback_context'],
        }
        return reduced_summary_blocks

    token_estimate = estimate_tokens(reduced_file_summary)
    reduced_file_hierarchy = summarize_file_hierarchy(
        file_hierarchy,
        (remaining_tokens - token_estimate)
    )
    reduced_summary_blocks = {
        "file_hierarchy": reduced_file_hierarchy,
        "file_summary": reduced_file_summary,
        "traceback": summary_blocks['traceback'],
        "traceback_context": summary_blocks['traceback_context'],
    }

    if estimate_tokens(reduced_summary_blocks) > max_tokens_out:
        raise ValueError("The total length of the summary blocks is greater"
                         "than the max_tokens_out")

    return reduced_summary_blocks


def format_summary(summary):
    """
    Format a summary dictionary into a string.

    Args:
        summary (dict): A dictionary of the directory's files and their summaries.

    Returns:
        str: The formatted summary.
    """

    formatted = []
    for file_path, content in summary.items():
        file_info = f"File: {file_path}"
        if isinstance(content, list):
            functions_str = '\n'.join([f"{str(func)}" for func in content])
            if len(functions_str) == 0:
                # functions_str = "No functions found"
                formatted.append(f"{file_info}\n")
            else:
                formatted.append(f"{file_info}\n```\n{functions_str}\n```\n")
        else:  # Assuming it's the full file content
            formatted.append(f"{file_info}\n```\n{content}\n```\n")
    return '\n'.join(formatted)


def split_file_summaries(file_summaries, max_chunk_tokens=2000):
    """
    Split a file summary into chunks of a certain number of tokens.

    Args:
        file_summaries (str): The file summary to split.
        max_chunk_tokens (int, optional): The maximum number of tokens per chunk.
            Defaults to 2000.

    Returns:
        list: The list of chunks.
    """
    summary_chunks = []
    current_chunk = ""
    current_chunk_tokens = 0

    for line in file_summaries.split("\n"):
        line_tokens = estimate_tokens(line)

        if current_chunk_tokens + line_tokens > max_chunk_tokens:
            summary_chunks.append(current_chunk.strip())
            current_chunk = ""
            current_chunk_tokens = 0

        current_chunk += f"{line}\n"
        current_chunk_tokens += line_tokens

    if current_chunk.strip():
        summary_chunks.append(current_chunk.strip())

    return summary_chunks


def summarize_file_summaries(file_summaries, max_tokens_out=4000):
    """
    Summarize a file summary.

    Args:
        file_summaries (str): The file summary to summarize.
        max_tokens_out (int, optional): The maximum number of tokens to output.
            Defaults to 4000.

    Returns:
        str: The summarized file summary.
    """

    if OPENAI_API_KEY is None:
        return file_summaries

    summary_chunks = split_file_summaries(file_summaries)
    summarized_chunks = []

    for chunk in summary_chunks:
        prompt = f"""Please provide a concise summary of the following codebase.
Highlight core files, classes, and functions.

{chunk}

Summary:
"""
        summary = call_openai_api(prompt, max_tokens_out)
        summarized_chunks.append(summary)

    # Combine summarized chunks
    combined_summary = "\n".join(summarized_chunks)

    # Check if combined summary fits within the token limit
    while estimate_tokens(combined_summary) > max_tokens_out:
        max_tokens_out -= 50
        summarized_chunks = summarize_file_summaries(combined_summary, max_tokens_out)
        combined_summary = "\n".join(summarized_chunks)

    return combined_summary


def summarize_file_hierarchy(file_hierarchy, max_tokens=4096):
    """
    Summarize a file hierarchy using OpenAI's API.

    Args:
        file_hierarchy (str): The file hierarchy to summarize.
        max_tokens (int, optional): The maximum number of tokens to output.
            Defaults to 4096.

    Returns:
        str: The summarized file hierarchy.
    """

    if OPENAI_API_KEY is None:
        return file_hierarchy

    prompt = f"""Please provide a concise file hierarchy.
Highlight core files, classes and functions.
Summarize directories with many files.

{file_hierarchy}

Summarized File Hierarchy:
"""
    return call_openai_api(prompt, max_tokens)
