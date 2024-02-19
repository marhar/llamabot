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

# Example usage
json1 = {
    "model": "ollama/llama2",
    "created_at": "2024-02-18T16:36:50.239761",
    "response": "Love is unpredictable and can happen to anyone, even fools. It's a universal emotion beyond logic and reason. Fools may fall in love because they are hopeful, vulnerable, or seeking connection and happiness. Ultimately, the heart wants what it wants, regardless of whether one is deemed a fool or not.",
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
