import sys
import argparse

def input_validation():
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



def main():
    args = input_validation()
    for name, value in vars(args).items():
        print (name, value)

if __name__== '__main__':
    main()