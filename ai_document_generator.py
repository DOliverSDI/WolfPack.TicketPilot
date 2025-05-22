from transformers import pipeline
import torch
from chat_log_data import ChatLogData
import os
from datetime import datetime

# Initialize the text generation pipeline with a Gemma model
# Note: "gemma 3 : 1b" is not a standard Hugging Face model name.
# Using "google/gemma-2b" as an example. Replace with the correct
# model identifier if "gemma 3 : 1b" refers to a specific one.
# Gemma models often require trust_remote_code=True.
# device_map="auto" helps in distributing the model across available hardware.
# torch_dtype can be used for optimization (e.g., torch.bfloat16 if supported).
try:
    model_name = "google/gemma-3-4b-it" # Replace if you have a specific "gemma 3 : 1b" identifier
    pipe = pipeline(
        'text-generation',
        model=model_name,
        torch_dtype=torch.bfloat16, # Use bfloat16 if Ampere GPU or newer
        trust_remote_code=True # Gemma models often require this
    )
except Exception as e:
    print(f"Error initializing the model pipeline: {e}")
    print("Please ensure you have an internet connection to download the model,")
    print("and that the 'transformers' and a backend (PyTorch/TensorFlow) are correctly installed.")
    pipe = None

def generate_service_document(chat_details):
    """
    Generates a concise service document based on chat details.

    Args:
        chat_details (dict): A dictionary containing information extracted
                             from the chat log. Expected keys:
                             'date', 'initial_request', 'resolution'.

    Returns:
        str: The generated document, or an error message if generation fails.
    """
    if not pipe:
        return "AI model pipeline is not available."

    # Define the prompt template with placeholders
    prompt_template = f"""
    You are an Information Mediator and an expert in Google Tag Manager and Google Analytics 4 who will create a concise report based on the following chat log details:
    Date of Interaction: {chat_details.get('date', 'N/A')}
    Ticket ID: {chat_details.get('ticket_id', 'N/A')}
    Initial Request: {chat_details.get('initial_request', 'N/A')}
    Summary of Current Status: {chat_details.get('request_updates', 'N/A')}
    
    After providing the report based on the prompt above, list out three possible next steps to resolve this issue.
"""

    try:
        # Generate the document.
        # For Gemma, you might need to adjust max_new_tokens or max_length.
        # Gemma models have a larger context window (e.g., 8192 tokens for gemma-2b/7b).
        # Using max_new_tokens is often preferred to control the length of the generated part.
        desired_output_tokens = 500 # Adjust as needed for conciseness

        generated_outputs = pipe(
            prompt_template,
            max_new_tokens=desired_output_tokens, # Controls the length of the new text
            num_return_sequences=1,
            pad_token_id=pipe.tokenizer.eos_token_id,
            do_sample=True, # Recommended for more creative/natural output
            temperature=0.5, # Adjust for creativity vs. factuality
            top_k=50,
            top_p=0.95
        )
        
        # Extract the generated text part
        generated_text = generated_outputs[0]['generated_text']
        # Remove the prompt from the generated text to get only the report
        report_text = generated_text[len(prompt_template):].strip()
        
        return report_text
    except Exception as e:
        return f"Error during text generation: {e}"