# CodeSumma

CodeSumma is an AI-powered code summarization tool that streamlines the development process by generating concise, token-limited, summaries of Python codebases. By simplifying AI-assisted development, CodeSumma enables developers to easily consult ChatGPT for help with debugging, adding features, or re-architecting portions of their code. CodeSumma is especially valuable when combined with autonomous agents like [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT), [BabyAGI](https://github.com/yoheinakajima/babyagi), or [JARVIS](https://github.com/microsoft/JARVIS).

## Table of Contents

- [CodeSumma](#codesumma)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [How It Works](#how-it-works)
  - [Installation](#installation)
    - [Command-line Installation](#command-line-installation)
  - [Usage](#usage)
    - [Python Usage](#python-usage)
    - [Command-line Usage](#command-line-usage)
    - [Options](#options)
  - [Examples](#examples)
  - [Case Studies](#case-studies)
    - [Summarize a remote repository](#summarize-a-remote-repository)
    - [Resolve bugs by adding a traceback](#resolve-bugs-by-adding-a-traceback)
  - [Troubleshooting](#troubleshooting)
  - [Future Roadmap](#future-roadmap)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Generate code summaries with a focus on architecture, functions, and files
- Extract traceback information to provide context for ChatGPT
- Easy-to-use command line interface
- Alias support for quick access
- Seamless integration with ChatGPT
- Open-source and community-driven

## How It Works

CodeSumma scans your Python codebase and generates summaries, providing crucial context for ChatGPT. It extracts code structure, classes, functions, dependencies, and traceback information to create comprehensive summaries. These summaries can then be used to consult ChatGPT for assistance with development tasks.

## Installation

1. Clone the repository:

```bash
gh repo clone ryanmac/CodeSumma
```

2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API Key in `.env`

```bash
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Command-line Installation

1. Confirm codesumma.sh script is executable:

```bash
chmod +x /path/to/codesumma/codesumma.sh
```

2. Add a preferred alias (`cs` or `codesumma`) to your `.bashrc` or `.zshrc`:

```bash
alias cs='bash /path/to/codesumma/scripts/codesumma.sh'
alias codesumma='bash /path/to/codesumma/scripts/codesumma.sh'
```

## Usage

You can use CodeSumma as a command-line tool or a Python library.

### Python Usage

```bash
python /path/to/CodeSumma/main.py
```

### Command-line Usage

To generate a summary of your Python codebase with guided prompts, initiate the shell script:

```bash
codesumma
```

Run in manual mode to be prompted for each argument. This is helpful to paste tracebacks to return relevant code snippets for additional context.

```bash
codesumma -m
```

### Options

Use arguments to focus your results.

```bash
positional arguments:
  input_path            Path to a Python file or a directory

options:
  -h, --help            Show this help message and exit
  -a, --all             Write out all code
  -cp, --copy           Copy output to clipboard - requires pyperclip)
  -i pattern [pattern ...], --ignore pattern [pattern ...]
                        Ignore patterns (e.g. "*.pyc")
  -m, --manual          Prompt user for all inputs. Helpful for pasting traceback.
  -o MAX_TOKENS_OUT, --max-tokens-out MAX_TOKENS_OUT
                        Maximum tokens for output summary
  -pf pattern [pattern ...], --print-full pattern [pattern ...]
                        Print full file content for files matching the pattern (e.g. "test_")
  -t [traceback_text], --traceback [traceback_text]
                        Provide traceback text for context or leave it empty to read from stdin
```

## Examples

Generate a summary under 4096 tokens of a Python codebase and export it to your clipboard, ignoring files matching the string `test`.

```bash
codesumma . --copy --ignore test --max-tokens-out 4096
```

Generate a summary of a remote GitHub repository in under 4096 tokens:

```bash
codesumma https://github.com/ryanmac/CodeSumma -ignore test -o 4096
```

<details>
  <summary>Result</summary>

  ````markdown
Context:

Directory Structure:
```
./
    .flake8
    README.md
    __init__.py
    main.py
    pyproject.toml
    requirements.txt
    scripts/
        codesumma.sh
    setup.py
    src/
        __init__.py
        cache.py
        file_processing.py
        openai_api.py
        summary.py
        traceback_parser.py
        utils.py
```

File Summary:
File: ./.flake8
```
This code is a configuration file for the `flake8` linter. It tells `flake8` to ignore certain files and directories (`.git`, `__pycache__`, `build`, `dist`) and to set the maximum line length to 88 characters.
```

File: ./requirements.txt

File: ./pyproject.toml
```
This is a codebase for a Python project called "CodeSumma." It requires the setuptools and wheel libraries, and has dependencies on Python 3.10, the OpenAI library, and the TikTok library. The project also uses the Python-Dotenv library for development.
```

File: ./__init__.py

File: ./README.md
```
CodeSumma is a tool that generates summaries of Python codebases. It extracts code structure, classes, functions, dependencies, and traceback information to create comprehensive summaries. These summaries can then be used to consult ChatGPT for assistance with development tasks.
```

File: ./setup.py

File: ./main.py
```
main()
```

File: ./scripts/codesumma.sh
```
The code above defines a function called `prompt_args` which prompts the user for input on various code summarization options. The user can input a path to the code they want to summarize, choose whether or not to summarize the code, input file patterns to ignore, input file patterns to include in the full code, and input a traceback to find relevant code snippets for. The code also defines a maximum length for the summary in BPE tokens.
```

File: ./src/cache.py
```
hash_key(prompt_object)
load_cache()
save_cache(cache)
get_cache(prompt_object, cache)
set_cache(prompt_object, response, cache)
```

File: ./src/__init__.py

File: ./src/openai_api.py
```
call_openai_api(prompt, max_tokens, model)
estimate_tokens(string, encoding_name)
trim_string_to_token_limit(string, max_tokens)
```

File: ./src/summary.py
```
run_summary(args)
process_class(cls)
generate_summary_from_python_file(file_path)
summarize_directory(dir_path, ignore_patterns, print_full_patterns)
summarize_blocks(summary_blocks, max_tokens_out)
format_summary(summary)
split_file_summaries(file_summaries, max_chunk_tokens)
summarize_file_summaries(file_summaries, max_tokens_out)
summarize_file_hierarchy(file_hierarchy, max_tokens)
```

File: ./src/utils.py
```
parse_arguments()
is_github_url(url)
Class: FunctionInfo
__init__(self, name, args, return_type)
__str__(self)
__eq__(self, other)
get_function_info(func_def)
```

File: ./src/file_processing.py
```
get_file_hierarchy(path, prefix, ignore_patterns)
format_file_hierarchy(path, ignore_patterns)
get_ignore_patterns(input_path, ignore_patterns)
check_ignore_patterns(path, ignore_patterns)
get_all_code(dir_path, ignore_patterns)
```

File: ./src/traceback_parser.py
```
get_function_context(file_path, line_number)
get_line_context(file_path, line_number, context)
parse_traceback(tb_str)
format_parsed_traceback(parsed_traceback)
```


  ````
</details>

```bash
codesumma https://github.com/Significant-Gravitas/Auto-GPT -o 4096 -i test
```

<details>
  <summary>Result</summary>

  ````markdown
Context:

Directory Structure:
```
./
    .coveragerc
    .devcontainer/
        Dockerfile
        devcontainer.json
    .dockerignore
    .flake8
    .isort.cfg
    .pre-commit-config.yaml
    .sourcery.yaml
    BULLETIN.md
    CODE_OF_CONDUCT.md
    CONTRIBUTING.md
    Dockerfile
    README.md
    autogpt/
        __init__.py
        __main__.py
        agent/
            __init__.py
            agent.py
            agent_manager.py
        api_manager.py
        app.py
        chat.py
        cli.py
        commands/
            __init__.py
            analyze_code.py
            audio_text.py
            command.py
            execute_code.py
            file_operations.py
            git_operations.py
            google_search.py
            image_gen.py
            improve_code.py
            times.py
            twitter.py
            web_playwright.py
            web_requests.py
            web_selenium.py
        config/
            __init__.py
            ai_config.py
            config.py
        configurator.py
        js/
            overlay.js
        json_utils/
            __init__.py
            json_fix_general.py
            json_fix_llm.py
            llm_response_format_1.json
            utilities.py
        llm_utils.py
        logs.py
        main.py
        memory/
            __init__.py
            base.py
            local.py
            milvus.py
            no_memory.py
            pinecone.py
            redismem.py
            weaviate.py
        models/
            base_open_ai_plugin.py
        modelsinfo.py
        plugins.py
        processing/
            __init__.py
            html.py
            text.py
        prompts/
            __init__.py
            generator.py
            prompt.py
        setup.py
        singleton.py
        speech/
            __init__.py
            base.py
            brian.py
            eleven_labs.py
            gtts.py
            macos_tts.py
            say.py
        spinner.py
        token_counter.py
        types/
            openai.py
        url_utils/
            __init__.py
            validators.py
        utils.py
        workspace/
            __init__.py
            workspace.py
    azure.yaml.template
    benchmark/
        __init__.py
        benchmark_entrepreneur_gpt_with_difficult_user.py
    codecov.yml
    data_ingestion.py
    docker-compose.yml
    docs/
        code-of-conduct.md
        configuration/
            imagegen.md
            memory.md
            search.md
            voice.md
        contributing.md
        imgs/
            openai-api-key-billing-paid-account.png
        index.md
        plugins.md
        setup.md
        usage.md
    main.py
    mkdocs.yml
    plugin.png
    plugins/
        __PUT_PLUGIN_ZIPS_HERE__
    pyproject.toml
    requirements.txt
    run.bat
    run.sh
    run_continuous.bat
    run_continuous.sh
    scripts/
        __init__.py
        check_requirements.py
        install_plugin_deps.py
```

File Summary:
The Auto-GPT project is a tool that allows users to train their own language models using the OpenAI API. The project includes a number of files that set up the Azure API, install dependencies, format code, lint code, run tests, and so on. The project also includes a number of files that define the website, navigation, theme, and license for the project.
- The Auto-GPT Plugin Template can be used as a starting point for creating new plugins.
- The /docs/contributing.md file provides guidelines and best practices for contributing to Auto-GPT.
- The /docs/configuration/search.md file
The codebase defines a series of classes and methods for an AI agent. The agent interacts with a user via an interface, and uses a memory backend to store
The codebase consists of several files responsible for different tasks related to text-to-speech synthesis, prompt generation, and command execution. The main files and classes are:

- /autogpt/speech/macos_tts.py: MacOSTTS class responsible for synthesizing speech on macOS
- /autogpt/speech/say.py: say_text function responsible for synthesizing speech on all platforms
- /autogpt/speech/base.py: VoiceBase class responsible for synthesizing speech on all platforms
- /autogpt/prompts/generator.py: PromptGenerator class responsible for generating prompts
- /autogpt/commands/command.py: Command class responsible for representing individual commands, and CommandRegistry class responsible for managing all commands
- /autogpt/commands/web_requests.py: scrape_text and scrape_links functions responsible for scraping text and links from websites
- /autogpt/commands/file_operations.py: read_file, write_to_file, and delete_file functions responsible for reading, writing, and deleting files
- /autogpt/commands/execute_code.py: execute_python_file function responsible for executing Python code
- /scripts/check_requirements.py: main function responsible for checking requirements
- /scripts/install_plugin_deps.py: install_plugin_dependencies function responsible for installing plugin dependencies

Summary length: 5057 characters, 2319 tokens
  ````
</details>

Copy a summary of a remote repository to the clipboard, ignoring the readme, and including full code for files matching `main` and `test_file`.

```bash
codesumma https://github.com/ryanmac/CodeSumma --print-full main test_file --ignore readme -cp
```

<details>
  <summary>Result</summary>

  ````bash
Context:

Directory Structure:
```
./
    .flake8
    __init__.py
    main.py
    pyproject.toml
    requirements.txt
    scripts/
        codesumma.sh
    setup.py
    src/
        __init__.py
        cache.py
        file_processing.py
        openai_api.py
        summary.py
        traceback_parser.py
        utils.py
    tests/
        __init__.py
        conftest.py
        test_file_processing.py
        test_files/
            test_file.py
            test_file2.py
            traceback.txt
        test_summary.py
        test_traceback_parser.py
```

File Summary:
File: /.flake8
```
This is a configuration file for the flake8 linter. The file specifies that certain directories and files should be excluded from linting, and that the maximum line length should be 88 characters.
```

File: /requirements.txt

File: /pyproject.toml
```
This is a configuration file for the Poetry build system. It requires the setuptools and wheel packages, and defines the name, version, description, authors, and license for the project. It also defines the dependencies for the project, which include Python 3.10, the OpenAI package, and the TikTok package. Finally, it defines the dev-dependencies for the project, which include Pytest and Flake8.
```

File: /__init__.py

File: /setup.py

File: /main.py
```
import pyperclip
from src.summary import run_summary
from src.utils import parse_arguments


def main():

    args = parse_arguments()

    # print(args)

    formatted_summary, num_tokens = run_summary(args)

    print(formatted_summary)

    print(f"Summary length: {len(formatted_summary)} characters, {num_tokens} tokens")

    if args.copy:
        try:
            pyperclip.copy(formatted_summary)
            print(f"Copied {num_tokens} tokens to the clipboard.")
        except ImportError:
            print("pyperclip package not found."
                  "Please install it to use the clipboard feature.")


if __name__ == '__main__':
    main()

```

File: /tests/test_file_processing.py
```
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

```

File: /tests/test_traceback_parser.py
```
test_get_function_context()
test_get_line_context()
test_parse_traceback()
test_format_parsed_traceback()
```

File: /tests/conftest.py

File: /tests/__init__.py

File: /tests/test_summary.py
```
test_generate_summary_from_python_file()
test_get_function_info()
test_summarize_directory()
test_format_summary()
```

File: /tests/test_files/traceback.txt

File: /tests/test_files/test_file.py
```
def add(a, b):
    return a + b


def divide(a, b):
    return a / b

```

File: /tests/test_files/test_file2.py
```
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def modulus(a, b):
    return a % b

```

File: /scripts/codesumma.sh
```
The code above prompts the user for various input arguments that will be used to summarize code. The user can input a path to the code they want to summarize, choose whether or not to summarize the code, input file patterns to ignore, input file patterns to include in the full code, and input a traceback. The code will then summarize the code based on the inputted arguments.
```

File: /src/cache.py
```
hash_key(prompt_object)
load_cache()
save_cache(cache)
get_cache(prompt_object, cache)
set_cache(prompt_object, response, cache)
```

File: /src/__init__.py

File: /src/openai_api.py
```
call_openai_api(prompt, max_tokens, model)
estimate_tokens(string, encoding_name)
trim_string_to_token_limit(string, max_tokens)
```

File: /src/summary.py
```
run_summary(args)
process_class(cls)
generate_summary_from_python_file(file_path)
summarize_directory(dir_path, ignore_patterns, print_full_patterns)
summarize_blocks(summary_blocks, max_tokens_out)
format_summary(summary)
split_file_summaries(file_summaries, max_chunk_tokens)
summarize_file_summaries(file_summaries, max_tokens_out)
summarize_file_hierarchy(file_hierarchy, max_tokens)
```

File: /src/utils.py
```
parse_arguments()
is_github_url(url)
Class: FunctionInfo
__init__(self, name, args, return_type)
__str__(self)
__eq__(self, other)
get_function_info(func_def)
```

File: /src/file_processing.py
```
get_file_hierarchy(path, prefix, ignore_patterns)
format_file_hierarchy(path, ignore_patterns)
get_ignore_patterns(input_path, ignore_patterns)
check_ignore_patterns(path, ignore_patterns)
get_all_code(dir_path, ignore_patterns)
```

File: /src/traceback_parser.py
```
get_function_context(file_path, line_number)
get_line_context(file_path, line_number, context)
parse_traceback(tb_str)
format_parsed_traceback(parsed_traceback)
```


  ````
</details>

Let CodeSumma prompt you for each argument:

```bash
codesumma --manual
```

This initiatiates manual mode, prompting your for each argument that CodeSumma supports.

<details>
  <summary>Example</summary>

  ```markdown
**CodeSumma**
Hit enter for default

What is the path to the code you want to summarize?
Input Path (Default: .): 

Would you like to summarize the code? **Yes** will summarize the code, **No** will print out all code.
Summarize Code (Default: Yes): 

Are there any files patterns you want to ignore?
Ignore Patterns (Default: .git, .env, .pkl, pycache): 

Are there any files you need the full code for?
Full File Patterns (Default: None): 

Is there a traceback you'd like to find relevant code snippets for?
Enter the traceback (Default: None), press ENTER twice to finish:


How long can the summary be (in BPE tokens)?
Max Tokens Out (Default: 4096):
  ```
</details>


## Case Studies

### Summarize a remote repository

This can be useful to give ChatGPT context to add a feature or develop an integration.

```bash
codesumma https://github.com/ryanmac/CodeSumma --all --ignore test
```

<details>
  <summary>Result</summary>
  
  ````markdown
Context:

Directory Structure:
```
./
    .flake8
    README.md
    __init__.py
    main.py
    pyproject.toml
    requirements.txt
    scripts/
        codesumma.sh
    setup.py
    src/
        __init__.py
        cache.py
        file_processing.py
        openai_api.py
        summary.py
        traceback_parser.py
        utils.py
```

File Summary:
File: ./.flake8
```
This code is a configuration file for the `flake8` linter. It tells `flake8` to ignore certain files and directories (`.git`, `__pycache__`, `build`, `dist`) and to set the maximum line length to 88 characters.
```

File: ./requirements.txt

File: ./pyproject.toml
```
This is a codebase for a Python project called "CodeSumma." It requires the setuptools and wheel libraries, and has dependencies on Python 3.10, the OpenAI library, and the TikTok library. The project also uses the Python-Dotenv library for development.
```

File: ./__init__.py

File: ./README.md
```
CodeSumma is an AI-powered code summarization tool that streamlines the development process by generating concise, token-limited, summaries of Python codebases. By simplifying AI-assisted development, CodeSumma enables developers to easily
```

File: ./setup.py

File: ./main.py
```
main()
```

File: ./scripts/codesumma.sh
```
The code above is a Bash script that calls a Python script, `main.py`, with a variety of arguments. The `input_path` argument is the path to the code that will be summarized. The `all_arg` flag tells the Python script to print out all code. The `ignore_arg` flag tells the Python script to ignore certain files. The `full_file_patterns_arg` flag tells the Python script to print out the full code for certain files. The `traceback_arg` flag tells the Python script to find relevant code snippets for a traceback. The `max_tokens_out_arg` flag tells the Python script the maximum length of the summary.
```

File: ./src/cache.py
```
hash_key(prompt_object)
load_cache()
save_cache(cache)
get_cache(prompt_object, cache)
set_cache(prompt_object, response, cache)
```

File: ./src/__init__.py

File: ./src/openai_api.py
```
call_openai_api(prompt, max_tokens, model)
estimate_tokens(string, encoding_name)
trim_string_to_token_limit(string, max_tokens)
```

File: ./src/summary.py
```
run_summary(args)
process_class(cls)
generate_summary_from_python_file(file_path)
summarize_directory(dir_path, ignore_patterns, print_full_patterns)
summarize_blocks(summary_blocks, max_tokens_out)
format_summary(summary)
split_file_summaries(file_summaries, max_chunk_tokens)
summarize_file_summaries(file_summaries, max_tokens_out)
summarize_file_hierarchy(file_hierarchy, max_tokens)
```

File: ./src/utils.py
```
parse_arguments()
is_github_url(url)
Class: FunctionInfo
__init__(self, name, args, return_type)
__str__(self)
__eq__(self, other)
get_function_info(func_def)
```

File: ./src/file_processing.py
```
get_file_hierarchy(path, prefix, ignore_patterns)
format_file_hierarchy(path, ignore_patterns)
get_ignore_patterns(input_path, ignore_patterns)
check_ignore_patterns(path, ignore_patterns)
get_all_code(dir_path, ignore_patterns)
```

File: ./src/traceback_parser.py
```
get_function_context(file_path, line_number)
get_line_context(file_path, line_number, context)
parse_traceback(tb_str)
format_parsed_traceback(parsed_traceback)
```

Summary length: 3311 characters, 1181 tokens
  ````
</details>

### Resolve bugs by adding a traceback

Run CodeSumma in manual mode to paste in your traceback:

```bash
codesumma -m
```

Answer the prompts to add your traceback:

<details>
  <summary>Example</summary>

  ````markdown
**CodeSumma**
Hit enter for default

What is the path to the code you want to summarize?
Input Path (Default: .): tests/test_files

Would you like to summarize the code? **Yes** will summarize the code, **No** will print out all code.
Summarize Code (Default: Yes): 

Are there any files patterns you want to ignore?
Ignore Patterns (Default: .git, .env, .pkl, pycache): 

Are there any files you need the full code for?
Full File Patterns (Default: None): 

Is there a traceback you'd like to find relevant code snippets for?
Enter the traceback (Default: None), press ENTER twice to finish:
Traceback (most recent call last):
File "tests/test_files/test_file.py", line 5, in divide
return a / b
        ~~^~~
ZeroDivisionError: division by zero


How long can the summary be (in BPE tokens)?
Max Tokens Out (Default: 4096): 
  ````
</details>

<details>
  <summary>Result</summary>

  ````markdown
CodeSumma
Context:

Directory Structure:
```
test_files/
    test_file.py
    test_file2.py
    traceback.txt
```

File Summary:
File: tests/test_files/traceback.txt

File: tests/test_files/test_file.py
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


Traceback:
```
Traceback (most recent call last):
File "tests/test_files/test_file.py", line 5, in divide
return a / b
        ~~^~~
ZeroDivisionError: division by zero

```

Traceback Context:
```
File: tests/test_files/test_file.py
Line: 5
Function: divide
Summary: divide(a, b)
def divide(a, b):
```

Resolve this error.

Summary length: 663 characters, 291 tokens

  ````
</details>

## Troubleshooting

If you encounter issues with your alias or environment variables, check your shell configuration file (e.g., `.bashrc` or `.zshrc`) and ensure that the correct alias and environment variables are set.

If you experience problems with the OpenAI API key, verify that it's correctly entered in the .env file in the project directory.

## Future Roadmap

- PyPI Package install
- Support for other programming languages (JavaScript, Solidity, Rust, Go)
- Support for additional AI platforms and LLMs
- Customizable model selection (currently code summaries run only `text-davinci-002`)
- Improved traceback analysis
- Enhanced code summarization features
- Customizable summary templates

## Contributing

We welcome contributions from the community! If you'd like to contribute to CodeSumma, follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your feature"`
4. Push your branch to your fork: `git push origin feature/your-feature-name`
5. Create a pull request to the original repository

Before submitting your pull request, please ensure that your code adheres to the project's coding standards and that all tests pass.

## License

CodeSumma is released under the MIT License.