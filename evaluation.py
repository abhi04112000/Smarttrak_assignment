import time
from bert_score import score
from code_assistant import complete_code, debug_code, get_documentation

def evaluate_agent(test_cases):
    total_cases = len(test_cases)
    correct_cases = 0
    total_time = 0
    bert_scores = []

    for case in test_cases:
        prompt = case['prompt']
        expected_output = case['expected_output']
        task = case['task']

        start_time = time.time()
        if task == "Code Completion":
            response = complete_code(prompt)
        elif task == "Debugging Assistance":
            response = debug_code(prompt)
        elif task == "Documentation Retrieval":
            response = get_documentation(prompt)
        else:
            continue

        end_time = time.time()
        response_time = end_time - start_time
        total_time += response_time

        if response.strip() == expected_output.strip():
            correct_cases += 1

        # Calculate BERT score
        bert_score = score([expected_output], [response], lang='en', verbose=False)[0].item()
        bert_scores.append(bert_score)

    accuracy = (correct_cases / total_cases) * 100
    avg_response_time = total_time / total_cases
    avg_bert_score = sum(bert_scores) / len(bert_scores)

    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Average BERT Score: {avg_bert_score:.4f}")

    if accuracy < 80:
        print("Potential Improvements:")
        print("- Fine-tune the GPT model on a larger and more diverse dataset related to coding and programming.")
        print("- Improve the prompt engineering to provide more context and clarity.")

    if avg_response_time > 5:
        print("Potential Optimizations:")
        print("- Implement caching mechanisms to store and reuse common responses.")
        print("- Explore more efficient GPT models or adjust the model parameters for faster inference.")

    if avg_bert_score < 0.8:
        print("Potential Improvements:")
        print("- Enhance the prompt filtering and post-processing techniques to improve the quality of responses.")
        print("- Explore fine-tuning the GPT model on a dataset specific to the given task.")

# Test cases
if __name__ == "__main__":
    test_cases = [
        {
            "prompt": "def greet(name):\n    print('Hello, ', name)",
            "expected_output": "def greet(name):\n    print('Hello, ', name)\n",
            "task": "Code Completion"
        },
        {
            "prompt": "Traceback (most recent call last):\n  File 'example.py', line 5, in <module>\n    print(x)\nNameError: name 'x' is not defined",
            "expected_output": "The error 'NameError: name 'x' is not defined' occurs when you try to use a variable that has not been defined or assigned a value. To fix this error, you need to make sure that you have defined and assigned a value to the variable 'x' before attempting to use it.",
            "task": "Debugging Assistance"
        },
        {
            "prompt": "str.replace() method in Python",
            "expected_output": "The `str.replace()` method in Python is used to replace occurrences of a substring within a string with another substring. It takes two arguments: the substring to be replaced, and the substring to replace it with. Here's the syntax: `str.replace(old, new, count)` - `old` is the substring to be replaced, `new` is the substring to replace it with, and `count` (optional) is the maximum number of occurrences to replace. If `count` is not provided, all occurrences will be replaced.",
            "task": "Documentation Retrieval"
        }
    ]

    evaluate_agent(test_cases)