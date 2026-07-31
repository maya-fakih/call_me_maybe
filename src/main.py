import sys
import argparse
import json
from typing import Any

def input_validation() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default= "data/input/functions_definition.json"
    )
    parser.add_argument(
        "--input",
        default = "data/input/function_calling_tests.json"
    )
    parser.add_argument(
        "--output",
        default = "data/output/function_calls.json"
    )
    return parser.parse_args()

def json_loader(args: argparse.Namespace) -> list[dict[str, Any]]:
    with open(args.functions_definition) as f:
        return json.load(f)

def main():
    args: argparse.Namespace = input_validation()
    for name, value in vars(args).items():
        print (name, value)
    try:
        functions = json_loader(args)
    except Exception as e:
        print(e)
        exit(1)


if __name__== '__main__':
    main()