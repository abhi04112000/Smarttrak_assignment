import gradio as gr
import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key_local = os.getenv('my_api_key')
openai.api_key = api_key_local


def bot_response(prompt, engine="gpt-3.5-turbo"):
    # Create a chat message with a user role
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[{"role": "user", "content": prompt}]
    )
    # Return the generated text
    return response.choices[0].message["content"].strip()

def generate_python_code(query):
    prompt = f"""Given that you are python coder ,you have to generate the code according to the query given by user

{query}

Return the full code as a string."""
    return bot_response(prompt)
 
# Function to complete code
def complete_code(partial_code):
    prompt = f"""Given the following partial Python code, complete it to make it a valid Python program:

{partial_code}

Return the completed code as a string."""
    return bot_response(prompt)

# Debugging assistance function
def debug_code(error_message):
    prompt = f"Suggest a fix for this error message:\n{error_message}"
    return bot_response(prompt)

# Documentation retrieval function
def get_documentation(query):
    prompt = f"""Provide documentation for:\n{query}

and provide the seperate link for the query inside the output that can be opened on click"""
    return bot_response(prompt)


# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Code Agent")
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(lines=10, label="Code/Query", placeholder="Enter your code or query here...")
            task_selection = gr.Radio(choices=["Generate python code","Code Completion", "Debugging Assistance", "Documentation Retrieval"], label="Task", info="Select the task you need assistance with.")
        with gr.Column():
            output_text = gr.Textbox(lines=10, label="Output")
    submit_button = gr.Button("Submit")
    with gr.Row():
        clear_button = gr.Button("Clear")

    def handle_submit(input_text, task_selection):
        if task_selection == "Generate python code":
            return generate_python_code(input_text)
        elif task_selection == "Code Completion":
            return complete_code(input_text)
        elif task_selection == "Debugging Assistance":
            return debug_code(input_text)
        elif task_selection == "Documentation Retrieval":
            return get_documentation(input_text)


    submit_button.click(handle_submit, inputs=[input_text, task_selection], outputs=output_text)
    clear_button.click(lambda: [input_text.update(value=""), output_text.update(value=""), task_selection.update(value="Code Completion")], inputs=None, outputs=None)

# Launching the interface
demo.launch(share=True,port=8000)
