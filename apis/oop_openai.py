import openai
import os

class OOP_Openai:
    def __init__(self, 
                 system_prompt: str = None, 
                 model: str = 'gpt-4o',
                 api_key: str = None
                 ):
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

    def __can_respond(self) -> bool:
        # Ensures the last message is from a user so we're not generating when we're not supposed to
        return self.chat_log[-1]['role'] == 'user'
    
    def __ephemeral_gen(self) -> str:
        # Generates a message from the assistant with no history by default
        if not self.__can_respond():
            raise ValueError("Not ready to respond because last message was not a user message.")
        
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            messages=self.chat_log,
            # temperature=0.7,
            model=self.model
        ).choices[0].message.content
        client.close()
        return response

    def add_user_message(self, user_message: str):
        # Puts a user message at the end of the chat but doesn't generate anything
        self.chat_log.append({
            'role': 'user',
            'content': user_message
        })

    def run_assistant_turn(self) -> str:
        # Generates the assistant message
        self.chat_log.append({
            'role': 'assistant',
            'content': self.__ephemeral_gen()
        })
        return self.chat_log[-1]['content'] # Return the AI generated text
    
    def __str__(self):
        # Returns a formatted string of the chat history
        chat_history_string = ""

        for message in self.chat_log:
            chat_history_string += f"{message['role'].upper()}: {message['content']}\n"

        return chat_history_string
