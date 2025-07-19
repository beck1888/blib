from openai import OpenAI

def one_off_prompt(prompt: str, api_key: str = None) -> str:
    """Allows you to quickly send a prompt to gpt-4o if all you need is a quick ai response. 
    Make sure to pass an API key if it's not loaded in your env."""


    if api_key is None:
        client = OpenAI()
    else:
        # if a key was passed
        client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    ).choices[0].message.content

    # Filter response
    import string
    okay = 'abcdefghijklmnopqrstuvwxyz0123456789!?"' + "'"

    final_response = ''
    for char in response:
        if char in okay:
            final_response += char

    return final_response