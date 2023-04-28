#!/bin/bash

function prompt_args() {
  printf "\033[1;36m**CodeSumma**\033[0m\n"
  printf "Hit enter for default\n\n"

  printf "What is the path to the code you want to summarize?\n"
  read -p "Input Path (Default: .): " input_path
  input_path=${input_path:-.}

  printf "\nWould you like to summarize the code? **Yes** will summarize the code, **No** will print out all code.\n"
  read -p "Summarize Code (Default: Yes): " summarize_code
  summarize_code=${summarize_code:-Yes}
  if [ "$summarize_code" != "Yes" ]; then
    all_arg="--all"
  fi

  printf "\nAre there any files patterns you want to ignore?\n"
  read -p "Ignore Patterns (Default: .git, .env, .pkl, pycache): " ignore_patterns
  if [ -n "$ignore_patterns" ]; then
    ignore_arg="--ignore $ignore_patterns"
  fi

  printf "\nAre there any files you need the full code for?\n"
  read -p "Full File Patterns (Default: None): " full_file_patterns
  if [ -n "$full_file_patterns" ]; then
    full_file_patterns_arg="--print-full $full_file_patterns"
  fi

  printf "\nIs there a traceback you'd like to find relevant code snippets for?\n"
  echo "Enter the traceback (Default: None), press ENTER twice to finish:"
  traceback=""
  while :; do
    IFS= read -r line
    if [ -z "$line" ]; then
      break
    fi
    traceback+="$line"$'\n'
  done
  if [ -n "$traceback" ]; then
    traceback_arg="--traceback '$traceback'"
  fi

  printf "\nHow long can the summary be (in BPE tokens)?\n"
  read -p "Max Tokens Out (Default: 4096): " max_tokens_out
  max_tokens_out=${max_tokens_out:-4096}
  max_tokens_out_arg="--max-tokens-out $max_tokens_out"
}

input_path="."
all_arg=""
copy_arg=""
ignore_arg=""
manual_mode=false
max_tokens_out_arg=""
print_full_arg=""
traceback_arg=""

while [[ $# -gt 0 ]]
do
  arg="$1"
  case $arg in
    --all|-a)
      all_arg="--all"
      shift
      ;;
    --copy|-cp)
      copy_arg="--copy"
      shift
      ;;
    --ignore|-i)
      shift
      while [[ -n "$1" && "$1" != -* ]]; do
        if [ -z "$ignore_arg" ]; then
          ignore_arg="--ignore $1"
        else
          ignore_arg="$ignore_arg,$1"
        fi
        shift
      done
      ;;
    --manual|-m)
      manual_mode=true
      shift
      ;;
    --max-tokens-out|-o)
      shift
      max_tokens_out_arg="--max-tokens-out $1"
      shift
      ;;
    --print-full|-pf)
      shift
      while [[ -n "$1" && "$1" != -* ]]; do
        if [ -z "$print_full_arg" ]; then
          print_full_arg="--print-full $1"
        else
          print_full_arg="$print_full_arg,$1"
        fi
        shift
      done
      ;;
    --traceback|-t)
      shift
      if [[ -n "$1" && "$1" != -* ]]; then
        traceback_arg="--traceback '$1'"
        shift
      else
        traceback_arg="--traceback"
      fi
      ;;
    *)
      input_path="$1"
      shift
      ;;
  esac
done

input_path=${input_path:-.}

if [ "$manual_mode" = true ]; then
  prompt_args
fi

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check for the availability of 'python3' and 'python'
PYTHON_CMD="python"
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif ! command -v python >/dev/null 2>&1; then
  echo "Error: python or python3 not found in your PATH."
  exit 1
fi

# Call the Python script with the proper arguments
printf "\033[1;36mCodeSumma\033[0m\n"
echo "$PYTHON_CMD $script_dir/../main.py $input_path $all_arg $copy_arg $ignore_arg $print_full_arg $traceback_arg $max_tokens_out_arg ${@/--manual/}"
eval "$PYTHON_CMD $script_dir/../main.py \"$input_path\" $all_arg $copy_arg $ignore_arg $print_full_arg $traceback_arg $max_tokens_out_arg ${@/--manual/}"