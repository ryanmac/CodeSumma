import pyperclip
from summary import run_summary
from utils import parse_arguments


def main():

    args = parse_arguments()

    print(args)

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
