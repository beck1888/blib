# Beck's Library (blib)

This project is a collection of python scripts I use a lot. I've refactored many with ChatGPT to make it more clear what they do.

Please note that this codebase if written with macOS usage in mind. Some functions won't work on other operating systems.

## Install
To install this codebase, run this script. It will clone the code you need into `blib/` and get rid of anything else.
```zsh
curl -sSL https://raw.githubusercontent.com/beck1888/blib/refs/heads/main/scripts/install.zsh | zsh
```

To update this "library", run the install command again.

## Example
```python
# Example usage of multiple functions

# Import buried functions from the blib
from blib.termio.terminal import Spinner
from blib.apis.onepw import get_openai_api_key
from blib.macOS_tools.applescript_dialogs import popup_ask_for_input, popup_show_message
from blib.apis.easy_openai import quick_prompt

# Get the OpenAI API Key
with Spinner("Fetching API key"):
    api_key = get_openai_api_key()

# Ask the user for input
user_question = popup_ask_for_input("Ask any question")
if user_question is None:
    popup_show_message("Please try again with a valid question")

# Call the OpenAI API
with Spinner("Asking ChatGPT"):
    ai_response = quick_prompt(user_question, 
                               api_key, 
                               system_prompt="Respond to the question in 10 words")

# Show the response
popup_show_message(ai_response)
```