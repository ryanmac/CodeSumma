from setuptools import setup, find_packages

setup(
    name="CodeSumma",
    version="0.1.0",
    description="CodeSumma is an AI-powered code summarization tool that streamlines"
                "the development process by generating concise, token-limited,"
                "summaries of Python codebases.",
    author="Ryan Mac",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "flake8",
        "gitpython",
        "openai",
        "pyperclip",
        "pytest",
        "python-dotenv",
        "tiktoken",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11.2",
    ],
)
