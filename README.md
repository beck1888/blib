# Beck's Junkdrawer

This project is a collection of python scripts I use a lot. I've refactored many with ChatGPT to make it more clear what they do.

Please note that this codebase if written with macOS usage in mind. Some functions won't work on other operating systems.

## Install
To install this codebase, run this script. It will clone the code you need into `junkdrawer/` and get rid of anything else.
```zsh
curl -sSL https://raw.githubusercontent.com/beck1888/junkdrawer/refs/heads/main/scripts/install.zsh | zsh
```

You may also want to install the `requirements.txt` file. Alternatively, you can look at the source for just the files you want and just install those requirements. Please note that the install script removes any files that aren't `.py` or `.zsh` so the requirements file is only viewable on GitHub.

To update this "library", run the install command again.

## Example
```python
# Example usage of multiple functions

# Import buried functions from the junkdrawer
from junkdrawer.termio.terminal import Spinner
from junkdrawer.apis.onepw import get_openai_api_key
from junkdrawer.macOS_tools.applescript_dialogs import popup_ask_for_input, popup_show_message
from junkdrawer.apis.openai import quick_prompt

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