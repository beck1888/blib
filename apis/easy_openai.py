"""
openai.py

Provides a utility function to quickly send prompts to OpenAI's GPT-4o model.

This module contains:
- quick_prompt: A function to send a prompt to OpenAI's GPT-4o and return the response.
"""

from openai import OpenAI

def quick_prompt(prompt: str, api_key: str = None, **kwargs) -> str:
    """
    Sends a prompt to OpenAI's GPT-4o model and returns the response as a string.

    Args:
        prompt (str): The user prompt to send to the model.
        api_key (str, optional): OpenAI API key. If not provided, uses the key from the environment.
        **kwargs: Optional keyword arguments. Supports 'system_prompt' to prepend a system message.

    Keyword Args:
        system_prompt (str, optional): A system message to prepend to the chat history.

    Returns:
        str: The model's response as a string.

    Raises:
        openai.error.OpenAIError: If there is an issue with the API request.
    """

    # Init the client with the api key from env if not passed directly
    if api_key is None:
        client = OpenAI()
    else:
        # if a key was passed
        client = OpenAI(api_key=api_key)

    # Create the chat history (messages)
    chat_history = [
            {
                "role": "user",
                "content": prompt
            }
    ]

    # Appending optional system prompt
    if "system_prompt" in kwargs:
        system_prompt = kwargs["system_prompt"]
        chat_history.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )
        chat_history.reverse() # Puts the system prompt at the start

    # Call the API
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=chat_history
    ).choices[0].message.content

    # Make sure the client closes
    client.close()

    return response