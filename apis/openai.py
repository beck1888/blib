from openai import OpenAI

def one_off_prompt(prompt: str, api_key: str = None, **kwargs) -> str:
    """Allows you to quickly send a prompt to gpt-4o if all you need is a quick ai response. 
    Make sure to pass an API key if it's not loaded in your env."""

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