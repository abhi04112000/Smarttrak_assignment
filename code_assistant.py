import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key_local = os.getenv('my_api_key')
openai.api_key = api_key_local

def bot_response(prompt, engine="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()

def generate_python_code(query):
    prompt = f"""Given that you are a Python coder, you have to generate the code according to the query given by the user:

{query}

Return the full code as a string."""
    return bot_response(prompt)

def complete_code(partial_code):
    prompt = f"""Given the following partial Python code, complete it to make it a valid Python program:

{partial_code}

Return the completed code as a string."""
    return bot_response(prompt)

def debug_code(error_message):
    prompt = f"Suggest a fix for this error message:\n{error_message}"
    return bot_response(prompt)

def get_documentation(query):
    prompt = f"""Provide documentation for:\n{query}

and provide the separate link for the query inside the output that can be opened on click"""
    return bot_response(prompt)

st.title("Code Agent")

code_or_query = st.text_area("Code/Query", height=200, value="Enter your code or query here...")
task_selection = st.radio("Task", ("Generate Python code", "Code Completion", "Debugging Assistance", "Documentation Retrieval"))

if st.button("Submit"):
    if task_selection == "Generate Python code":
        output_text = generate_python_code(code_or_query)
    elif task_selection == "Code Completion":
        output_text = complete_code(code_or_query)
    elif task_selection == "Debugging Assistance":
        output_text = debug_code(code_or_query)
    elif task_selection == "Documentation Retrieval":
        output_text = get_documentation(code_or_query)

    st.text_area("Output", value=output_text, height=200)

if st.button("Clear"):
    code_or_query = ""
    output_text = ""
    st.text_area("Output", value=output_text, height=200)
