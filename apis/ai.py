"""
This module provides the `AI` class for interacting with OpenAI's GPT models.

The `AI` class allows users to manage chat logs, send messages to the model, and retrieve responses. It supports both persistent chat history and temporary, context-free interactions.
"""

import openai
import os

class AI:
    """
    A class to interact with OpenAI's GPT models.

    Attributes:
        system_prompt (str): An optional system prompt to guide the model's behavior.
        model (str): The model to use for generating responses (default is 'gpt-4o').
        api_key (str): The API key for authenticating with OpenAI's API.
        chat_log (list): A list of messages representing the chat history.
    """

    def __init__(self, 
                 system_prompt: str = None, 
                 model: str = 'gpt-4o',
                 api_key: str = None
                 ):
        """
        Initializes the AI object with a system prompt, model, and API key.

        Args:
            system_prompt (str, optional): A system prompt to guide the model's behavior.
            model (str): The model to use for generating responses (default is 'gpt-4o').
            api_key (str, optional): The API key for authenticating with OpenAI's API. If not provided, it will be retrieved from the environment variable `OPENAI_API_KEY`.

        Raises:
            ValueError: If no API key is provided and the environment variable `OPENAI_API_KEY` is not set.
            ValueError: If an empty string is provided for the system prompt.
            TypeError: If the system prompt is not a string.
        """
        # API Key management
        if not api_key: # No explicitly provided key
            if "OPENAI_API_KEY" in os.environ.keys(): # But if there is an api key in the env
                self.api_key = os.environ.get('OPENAI_API_KEY')
            else: # There is not a provided API key
                raise ValueError("No API key provided and no api key in env.")
        else: # API key provided
            self.api_key = api_key

        # Create object's chat log
        self.chat_log = []
        
        # Append a system prompt to that chat log if provided
        self.system_prompt = system_prompt # Save for later for the temp chat method
        if system_prompt: # Parameter provided
            if isinstance(system_prompt, str): # String given (error checking)
                if len(system_prompt) > 0: # System prompt isn't empty
                    # Append in OpenAI format
                    self.chat_log.append({
                        'role': 'system',
                        'content': system_prompt
                    })
                else: # Empty string
                    raise ValueError("Empty string provided for system prompt.")
            else: # Non-string type
                raise TypeError(f"Invalid type given for object. Expected a string but got type: {str(type(system_prompt))}.")
        else: # No system prompt provided
            pass # No issue

        # Lock-in the model the user wants to use
        self.model = model
    
    def __ephemeral_gen(self, override_messages: list[dict[str, str]] = None) -> str:       
        """
        Generates a response from the model using the provided or default chat log.

        Args:
            override_messages (list[dict[str, str]], optional): A list of messages to override the default chat log. Each message should have 'role' and 'content' keys.

        Returns:
            str: The content of the model's response.
        """
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            messages=self.chat_log if override_messages is None else override_messages, # Appends custom messages if provided, otherwise uses the instance's messages
            # temperature=0.7,
            model=self.model
        ).choices[0].message.content
        client.close()
        return response
    
    def __run_assistant_turn(self) -> str:
        """
        Generates a response from the assistant and appends it to the chat log.

        Returns:
            str: The content of the assistant's response.
        """
        # Generates the assistant message
        self.chat_log.append({
            'role': 'assistant',
            'content': self.__ephemeral_gen()
        })
        return self.chat_log[-1]['content'] # Return the AI generated text

    def POST_to_chat(self, user_message: str) -> str:
        """
        Sends a user message to the chat and retrieves the assistant's response.

        Args:
            user_message (str): The user's message to send to the chat.

        Returns:
            str: The content of the assistant's response.
        """
        # Puts a user message at the end of the chat and responds to it
        self.chat_log.append({
            'role': 'user',
            'content': user_message
        })
        self.__run_assistant_turn()
        return self.chat_log[-1]['content'] # Return the AI generated text


    def temp_message(self, prompt: str) -> str:
        """
        Sends a temporary message to the model without saving it to the chat history.

        Args:
            prompt (str): The user's message to send to the model.

        Returns:
            str: The content of the model's response.
        """
        # Uses the client to respond to a chat but does NOT save to the chat history.
        # It also doesn't use past context. Just the system prompt if given and the user prompt.
        # Useful for prompts that need a response but shouldn't be referenced in further requests
        # and that shouldn't contain past context (sandboxed request).

        # Create the override message logs
        my_override_messages = []
        if self.system_prompt is not None: # Append system prompt first if given
            my_override_messages.append({
                'role': 'system',
                'content': self.system_prompt
            })
        # Then append the user's prompt
        my_override_messages.append({
            'role': 'user',
            'content': prompt
        })
        
        response = self.__ephemeral_gen(
            override_messages=my_override_messages
        )
        return response

        

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the chat history.

        Returns:
            str: The chat history as a formatted string.
        """
        # Returns a formatted string of the chat history
        chat_history_string = ""

        for message in self.chat_log:
            chat_history_string += f"{message['role'].upper()}: {message['content']}\n"

        return chat_history_string
