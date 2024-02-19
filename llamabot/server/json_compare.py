#!/usr/bin/env python
"""Compare two JSON inputs and return True if they have the same structure, False otherwise."""
import argparse
import json

def compare_json_by_type(json1, json2):
    # Check if both are dictionaries
    if not isinstance(json1, dict) or not isinstance(json2, dict):
        return False

    # Check if both have the same set of keys
    if set(json1.keys()) != set(json2.keys()):
        return False

    # Check the type of each value for each key
    for key in json1:
        # If types do not match
        if type(json1[key]) != type(json2[key]):
            return False

        # If the value is a dictionary, recurse
        if isinstance(json1[key], dict):
            if not compare_json_by_type(json1[key], json2[key]):
                return False

        # If the value is a list, check the type of each element in the list
        elif isinstance(json1[key], list):
            if not all(type(item) == type(json2[key][i]) for i, item in enumerate(json1[key])):
                return False

    # If all checks pass
    return True

test = """
# Example usage
json1 = {
    "model": "ollama/llama2",
    "created_at": "2024-02-18T16:36:50.239761",
    "response": "Love is unpredictable and can happen to anyone.",
    "done": True,
    "context": [0],
    "total_duration": 2486235000,
    "load_duration": 4000,
    "prompt_eval_count": 0,
    "prompt_eval_duration": 0,
    "eval_count": 0,
    "eval_duration": 2486231000
}

json2 = {
    "model": "example/example2",
    "created_at": "2023-12-15T11:22:33.445566",
    "response": "This is a different response, but the format is what matters here.",
    "done": False,
    "context": [1, 2, 3],  # Note the difference in length but not in type
    "total_duration": 1234567890,
    "load_duration": 5000,
    "prompt_eval_count": 1,
    "prompt_eval_duration": 100,
    "eval_count": 1,
    "eval_duration": 1234567000
}

print(compare_json_by_type(json1, json2))
"""

def main():
    parser = argparse.ArgumentParser(description='Compare two JSON inputs.')
    parser.add_argument('inputs', nargs=2, help='Two JSON strings or file paths.')
    parser.add_argument('--files', action='store_true', help='Indicates if inputs are file paths.')

    args = parser.parse_args()

    if args.files:
        # If --files is specified, treat inputs as file paths
        with open(args.inputs[0], 'r') as file1, open(args.inputs[1], 'r') as file2:
            json1 = json.load(file1)
            json2 = json.load(file2)
    else:
        # Otherwise, treat inputs as JSON strings
        json1 = json.loads(args.inputs[0])
        json2 = json.loads(args.inputs[1])

    result = compare_json_by_type(json1, json2)
    print(result)


if __name__ == '__main__':
    main()
