import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
import io
import unittest
from contextlib import redirect_stdout
import types
import re


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


def generate_code(task, llm):
    prompt = f"""
You are an AI programming assistant called Codkus. Your task is to help the user by generating high-quality Python code based on their requirements. Follow the guidelines below to ensure the best possible output:

Examples:
User: Write a Python function to calculate the factorial of a number.
Assistant: Here's a Python function to calculate the factorial of a number:

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

User: Create a Python function to check if a string is a palindrome.
Assistant: Here's a Python function to check if a string is a palindrome:

def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]

User: Write a Python program to find the sum of all elements in a list.
Assistant: Here's a Python program to find the sum of all elements in a list:

def sum_list(lst):
    total = 0
    for item in lst:
        total += item
    return total

numbers = [1, 2, 3, 4, 5]
result = sum_list(numbers)
print(f"Sum of list elements: {{result}}")

Guidelines:
1. Carefully analyze the user's requirements and ask for clarification if needed.
2. Use a problem-solving approach to break down the task into smaller sub-problems.
3. Write clean, efficient, and well-documented code following Python best practices.
4. Provide explanations and comments to make the code more understandable.
6. Optimize the code for performance, considering time and space complexity.
7. Consider edge cases and handle errors gracefully.
8. Format the code properly with consistent indentation and naming conventions.
9. Include relevant usage instructions if applicable. No examples in the code or a random print statement that is not needed.
10. Continuously learn and improve based on user feedback and new Python concepts.
11. Provide only the test case code, without any additional explanations or tags.

Task: {task + ". Be careful about edge cases. I do not care about any examples, just print plain code, according to the instructions."}
"""

    return llm.predict(prompt)


def clean_code(code, llm):
    prompt = f"""
    Code:
    ```
    {code}
    ```

    Please clean up the provided code by removing any trailing messages, irrelevant code, or syntax errors.
    Provide only the cleaned code, without any additional explanations or tags.
    """
    cleaned_code = llm.predict(prompt)
    
    # Remove any extra triple backticks from the cleaned code
    cleaned_code = cleaned_code.replace("```", "")
    
    return cleaned_code


def generate_test_cases(task, code, llm):
    prompt = f"""
    Task: {task}
    Code: {code.replace("```", "")}

    As a tester, your task is to create comprehensive test cases for the provided code.
    These test cases should encompass Basic, Edge, and Large Scale scenarios to ensure the code's
    robustness, reliability, and scalability. Provide only the test case code, without any additional explanations or tags.
    """
    test_cases = llm.predict(prompt)
    
    # Remove any extra triple backticks from the generated test cases
    test_cases = test_cases.replace("```", "")
    
    # Remove the phrase "Here are the test cases for the provided code:"
    test_cases = test_cases.replace("Here are the test cases for the provided code:", "").strip()
    
    return test_cases


def clean_test_cases(test_cases, llm):
    prompt = f"""
    Test Cases:
    ```
    {test_cases}
    ```

    Please clean up the provided test cases by removing any trailing messages, irrelevant code, or syntax errors.
    Ensure that all parentheses, brackets, and braces are properly balanced.
    Provide only the cleaned test case code, without any additional explanations or tags.
    """
    cleaned_test_cases = llm.predict(prompt)
    
    # Remove any extra triple backticks from the cleaned test cases
    cleaned_test_cases = cleaned_test_cases.replace("```", "").strip()
    
    # Check if parentheses, brackets, and braces are balanced
    if is_balanced(cleaned_test_cases):
        return cleaned_test_cases
    else:
        # If not balanced, ask the LLM to fix the test cases
        prompt = f"""
        Test Cases:
        ```
        {cleaned_test_cases}
        ```

        The provided test cases have unbalanced parentheses, brackets, or braces. Please fix the test cases to ensure proper syntax and balanced delimiters.
        Provide only the fixed test case code, without any additional explanations or tags.
        """
        fixed_test_cases = llm.predict(prompt)
        fixed_test_cases = fixed_test_cases.replace("```", "").strip()
        return fixed_test_cases

def is_balanced(code):
    stack = []
    opening_brackets = ["(", "[", "{"]
    closing_brackets = [")", "]", "}"]
    
    for char in code:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            if not stack:
                return False
            if opening_brackets[closing_brackets.index(char)] != stack.pop():
                return False
    
    return len(stack) == 0


def execute_code_and_tests(code, test_cases):
    # combine the code and test cases into a single string
    full_code = f"{code}\n\n{test_cases}"

    # redirect stdout to capture the output
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        try:
            # create a module dynamically
            module = types.ModuleType("test_module")
            # execute the code in the module's context
            exec(full_code, module.__dict__)
            # create a test suite from the module
            test_suite = unittest.TestLoader().loadTestsFromModule(module)
            # create a test runner and run the tests
            test_runner = unittest.TextTestRunner(stream=stdout, verbosity=2)
            test_runner.run(test_suite)
            output = stdout.getvalue()
        except Exception as e:
            output = f"Error: {str(e)}"

    return output


def fix_code(task, code, error, llm):
    prompt = f"""
    Task: {task}
    Code:
    ```
    {code}
    ```
    Error:
    ```
    {error}
    ```

    Please fix the code based on the provided error message. Ensure that the fixed code addresses the error and meets the task requirements.
    Provide only the fixed code, without any additional explanations or tags.
    """
    fixed_code = llm.predict(prompt)
    
    # remove any extra triple backticks from the fixed code
    fixed_code = fixed_code.replace("```", "").strip()
    
    return fixed_code


def main():
    st.set_page_config(page_title="Codkus", page_icon=":robot_face:")

    st.title("Codkus")
    st.write("Generate high-quality Python code with AI assistance.")

    # set up the customization options
    st.sidebar.title("Customization")
    model = st.sidebar.selectbox(
        "Choose a model",
        ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
    )

    llm = ChatGroq(
        temperature=0.05,
        groq_api_key=GROQ_API_KEY,
        model_name=model,
    )

    llm_cleaner = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
    )

    task = st.session_state.get("task", "")
    generated_code = st.session_state.get("generated_code", "")
    generated_test_cases = st.session_state.get("generated_test_cases", "")
    full_code = st.session_state.get("full_code", "")
    output = st.session_state.get("output", "")
    error_message = st.session_state.get("error_message", "")
    fixed_code_tooltip = st.session_state.get("fixed_code_tooltip", False)
    code_confirmed = st.session_state.get("code_confirmed", False)
    fixed_code = st.session_state.get("fixed_code", "")

    task = st.text_area("Enter the task:", value=task, height=200)

    if st.button("Generate Code"):
        if task:
            code = generate_code(task, llm)
            cleaned_code = clean_code(code, llm_cleaner)
            test_cases = generate_test_cases(task, cleaned_code, llm)
            cleaned_test_cases = clean_test_cases(test_cases, llm_cleaner)

            generated_code = cleaned_code
            generated_test_cases = cleaned_test_cases
            full_code = f"{cleaned_code}\n\n{cleaned_test_cases}"
            
            st.session_state["task"] = task
            st.session_state["generated_code"] = generated_code
            st.session_state["generated_test_cases"] = generated_test_cases
            st.session_state["full_code"] = full_code
            st.session_state["output"] = ""
            st.session_state["error_message"] = ""
            st.session_state["fixed_code_tooltip"] = False
            st.session_state["code_confirmed"] = False
            st.session_state["fixed_code"] = ""

    if generated_code or generated_test_cases:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Generated Code")
            st.code(generated_code, language="python")
        with col2:
            st.subheader("Generated Test Cases")
            st.code(generated_test_cases, language="python")

        st.subheader("Full Code (Code + Test Cases)")
        full_code = st.session_state.get("full_code", "")
        st.code(full_code, language="python")

    if st.button("Run Code and Tests"):
        output = execute_code_and_tests(generated_code, generated_test_cases)
        st.session_state["output"] = output
        st.subheader("Output")
        st.text(output)

        if "Error" in output:
            st.warning("An error occurred while running the code. Please copy the error message and use the 'Fix Code' button to resolve the issue.")

    if fixed_code_tooltip:
        st.info("The code has been fixed. Please re-run the tests to verify the changes.")

    error_message = st.text_area("Error Message", value=error_message, placeholder="Paste the error message here", height=100)
    st.session_state["error_message"] = error_message

    if st.button("Fix Code"):
        if error_message:
            fixed_code = fix_code(task, generated_code, error_message, llm)
            st.session_state["generated_code"] = fixed_code
            st.session_state["fixed_code"] = fixed_code
            full_code = f"{fixed_code}\n\n{generated_test_cases}"
            st.session_state["full_code"] = full_code
            st.experimental_rerun()
        else:
            st.warning("Please provide an error message to fix the code.")

    if fixed_code:
        st.subheader("Fixed Code")
        st.code(fixed_code, language="python")

    if st.button("Confirm Code"):
        st.session_state["code_confirmed"] = True
        st.success("Code confirmed! You can now download the code.")

    if st.session_state.get("code_confirmed", False):
        col1, col2 = st.columns(2)
        with col1:
            # download only the fixed code
            st.download_button(
                "Download Fixed Code",
                st.session_state.get("fixed_code", ""),
                file_name="fixed_code.py",
                mime="text/plain",
            )
        with col2:
            # download the full code (including testing)
            st.download_button(
                "Download Full Code (Code + Test Cases)",
                full_code,
                file_name="full_code.py",
                mime="text/plain",
            )


if __name__ == "__main__":
    main()