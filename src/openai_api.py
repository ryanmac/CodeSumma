# src/code_splitter.py
import tiktoken
import openai
import os
from dotenv import load_dotenv
from .cache import load_cache, get_cache, set_cache

cache = load_cache()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is not None:
    openai.api_key = OPENAI_API_KEY


def call_openai_api(
        prompt: str,
        max_tokens: int = 4096,
        model: str = "text-davinci-002"
        ) -> str:
    """
    Call the OpenAI API with the given prompt and return the response.

    Args:
        prompt (str): The prompt to use.
        max_tokens (int, optional): The maximum number of tokens to return.
        model (str, optional): The model to use. Defaults to "text-davinci-002".
        session_stats (SessionStats, optional): The session stats object.

    Returns:
        str: The response from the API.
    """

    if OPENAI_API_KEY is None:
        return prompt

    encoding_name = "gpt2"
    prompt_tokens = estimate_tokens(prompt, encoding_name)
    if prompt_tokens + max_tokens > 4096:
        max_tokens = 4096 - prompt_tokens

    prompt_object = (
        model,
        prompt,
        max_tokens,
        1,
        None,
        0.5,
    )
    response = get_cache(prompt_object, cache)
    if not response:
        # tokens_sent = estimate_tokens(prompt_object[1], encoding_name)
        response = openai.Completion.create(
            engine=prompt_object[0],
            prompt=prompt_object[1],
            max_tokens=prompt_object[2],
            n=prompt_object[3],
            stop=prompt_object[4],
            temperature=prompt_object[5],
        )
        # tokens_received = estimate_tokens(response.choices[0].text, encoding_name)
        set_cache(prompt_object, response, cache)

    return response.choices[0].text.strip()


def estimate_tokens(string: str, encoding_name: str = "gpt2") -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The string to count the tokens for.
        encoding_name (str): The encoding to use.

    Returns:
        int: The number of tokens.
    """

    if isinstance(string, list):
        return sum([estimate_tokens(s) for s in string])

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def trim_string_to_token_limit(string, max_tokens):
    """
    Trim a string to a certain number of tokens.

    Args:
        string (str): The string to trim.
        max_tokens (int): The maximum number of tokens to trim to.

    Returns:
        str: The trimmed string.
    """

    if estimate_tokens(string) <= max_tokens:
        return string

    split_string = string.split('\n')
    if len(split_string) == 1:
        split_string = string.split(' ')

    while estimate_tokens(split_string) > max_tokens:
        split_string.pop()

    return ' '.join(split_string)
