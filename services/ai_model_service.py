from django.conf import settings
from huggingface_hub import InferenceClient
import json
import re

# Initialize the InferenceClient with the API key for the Hugging Face Inference API
client = InferenceClient(api_key=settings.HUGGINGFACE_TOKEN)

def generate_code_review(project_title, project_description, file_name, file_content):
    '''
    This function sends a message to the AI model requesting code review suggestions for a given project and file content.
    The AI model is expected to provide at least 5 meaningful and specific suggestions or improvements for the code.
    The function returns the suggestions as a list of dictionaries, each containing the line number and suggestion, or an error if it occurs.
    '''
    # Add line numbers to the file content for clarity for the AI model
    numbered_content = "\n".join(
        f"{i + 1}: {line}" for i, line in enumerate(file_content.splitlines())
    )
    
    # Construct the message for the AI model, requesting code review suggestions
    message_content = f'''
    You are a programming expert that must respond strictly in JSON format. Do a concise code review on the following file and provide at least 5 meaningful suggestions or improvements. Each suggestion should include:
    - The current issue or limitation in a single sentence.
    - Why this issue matters in a single sentence.
    - A suggested fix in a single sentence.
    - The exact line number where the issue occurs, as provided in the file.
    
    It is crucial to use the correct line numbers as specified in the file content. Do not infer or estimate line numbers—use the line numbers explicitly provided at the beginning of each line.
    
    Keep the suggestions brief and focused, ideally less than 50 words each. Minimize using special characters that may interfere with JSON parsing.
    Limit the total response to 1000 tokens, and prioritize critical improvements.

    The project is called {project_title} with a description of: "{project_description}"
    The file is named {file_name} with the following content:
    {numbered_content}
    END OF FILE
    '''
    
    # Define JSON Schema for response validation
    response_format = {
        "type": "json",
        "value": {
            "type": "object",
            "properties": {
                "suggestions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "line_number": {"type": "integer"},
                            "suggestion": {"type": "string"},
                        },
                        "required": ["line_number", "suggestion"],
                    },
                },
            },
            "required": ["suggestions"],
        },
    }

    # Call the AI model
    messages = [{"role": "user", "content": message_content}]
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",  # Use the desired model
        messages=messages,  # Pass the message to the model
        max_tokens=4000,  # Increase max tokens for longer responses, should limit to 1000 in the response but set to 3000 just in case
        stream=True,  # Stream the response to avoid timeout
        temperature=0.4,  # Lower temperature for deterministic results
        response_format=response_format,  # Enforce JSON Schema validation
    )

    # Process the streaming response
    response_text = ""
    for chunk in stream:
        response_text += chunk.choices[0].delta.content

    # Attempt to parse the response as JSON
    try:
        suggestions = json.loads(response_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, handle the error
        print("Failed to parse JSON response")
        suggestions = None

    return suggestions.get("suggestions", [])

def generate_ai_answer(question_content):
    '''
    This function sends a message to the AI model with a question and returns the answer provided by the model.
    The AI model is expected to provide a detailed and relevant answer to the question.
    The function returns the answer as a string or an error if it occurs.
    '''
    # Construct the message for the AI model, requesting an answer to the question
    message_content = f'''
    You are a programming expert that only responds in plain text. Provide a detailed and relevant answer to the following question:
    {question_content}
    '''

    # Call the AI model
    messages = [{"role": "user", "content": message_content}] 
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct", # Use the desired model
        messages=messages, # Pass the message to the model
        max_tokens=1000, # Increase max tokens for longer responses
        stream=True, # Stream the response to avoid timeout
        temperature=0.8, # Lower temperature for more deterministic results
    )

    # Process the streaming response
    response_text = ""
    for chunk in stream:
        response_text += chunk.choices[0].delta.content

    return response_text
