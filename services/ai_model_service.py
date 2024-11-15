from django.conf import settings
from huggingface_hub import InferenceClient
import json
import re

# Initialize the InferenceClient with the API key for the Hugging Face Inference API
client = InferenceClient(api_key=settings.HUGGINGFACE_TOKEN)

def code_review(project_title, project_description, file_name, file_content):
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
    You are a programming expert that only responds in JSON. Do a detailed code review on the following file and provide at least 5 meaningful and specific suggestions or improvements. Each suggestion should include:
    - The current issue or limitation with the code.
    - Why this issue matters or how it affects performance, readability, or security.
    - A suggested fix with a brief explanation of the approach, and if possible, an example of how to implement it. 

    Respond only with valid JSON and in plain English, using only double quotes for strings. Avoid using double quotes within suggestions and avoid any special characters that could interfere with JSON parsing. Each suggestion should be an object containing "line_number" and "suggestion" attributes. Here is an example of the expected JSON format:
    [
    {{
    "line_number": 25,
    "suggestion": "Consider adding input validation for user email. Currently, there is no validation on the email field, which may allow invalid email formats to be used. Input validation can improve security and prevent incorrect data entry. One approach is to use a regular expression to check the email format. For example: if (!Patterns.EMAIL_ADDRESS.matcher(userEmail).matches()) {{ /* show error */ }}"
    }},
    {{
    "line_number": 44,
    "suggestion": "Using ViewBinding or DataBinding would eliminate the need for findViewById, which can clutter the code and lead to errors if IDs change. ViewBinding generates a binding class for each XML layout file, allowing direct access to views. This improves code readability and reduces boilerplate code. Example: val binding = FragmentCommentsSheetBinding.inflate(inflater, container, false); binding.commentText.text = 'example'."
    }},
    ...
    ]

    The project is called {project_title} with a description of: "{project_description}"
    Each line in the file begins with "a number: ", which corresponds to the line number. The file is named {file_name} with the following content:
    {numbered_content}
    END OF FILE
    Remember, only respond with valid JSON. Do not write an introduction or summary.
    '''

    # Call the AI model
    messages = [{"role": "user", "content": message_content}] 
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct", # Use the desired model
        messages=messages, # Pass the message to the model
        max_tokens=1000, # Increase max tokens for longer responses
        stream=True, # Stream the response to avoid timeout
        temperature=0.4, # Lower temperature for more deterministic results, more consistant at returning correct JSON
    )

    # Process the streaming response
    response_text = ""
    for chunk in stream:
        response_text += chunk.choices[0].delta.content

    # Attempt to parse the response as JSON
    try:
        # Try to load the JSON response
        suggestions = json.loads(response_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, attempt to extract JSON-like content
        json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
        # If a JSON-like structure is found, extract and load it
        if json_match:
            json_str = json_match.group(0)
            suggestions = json.loads(json_str)
        # If no JSON-like structure is found, handle the error
        else:
            suggestions = None

    return suggestions
