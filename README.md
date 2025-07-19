# Beck's Python Junk Drawer

Hi, and welcome to my "junk drawer" for my python code. In writing code over the years, I've amassed quite the collection of code I find myself using all the time. I've decided to lump it all into one standard "library" of sorts that I can quickly dump into my own projects.

This codebase has tools for many very different jobs, so I've tried to document what does what.

Also, I did use AI to help me clean up a lot of this code so other people can understand it. Just felt like I should mention that. And there is also a lot of code that I had written before, but I had AI help me refactor it for better readability and maintainability.

Finally, **this code is meant to be run on macOS.** Parts of it may work on other operating systems, but I haven't tested it there. Some code also assumes you have 1Password set up, certain API keys, etc. Without those, some of this code will not work.

## The "system" Folder

### terminal.py

The file `system/terminal.py` contains tools for interactions with the standard in/output, including spinners, rich(er) text formatting, and cursor manipulation. The classes you can use are:

1. **Cursor**

    Showing and hiding the cursor can be useful to enforce certain terminal styles.

    1. *show*: Makes the system cursor appear in the standard output
    2. *hide*: Makes the system cursor hide in the standard output

2. **Spinner**

    The spinner (as seen in similar functionality in tools like npm) is a great way to show your users that a task is working, but may take a while to complete.

    The spinner can be accessed using a `with` block like this:

    ```python
    with Spinner("Doing something cool"):
        ... # Your code here
    ```
    Remember to unindent after your done with the code to run in that spinner. The spinner will automatically show and hide the cursor as well as track execution status and time.

    The standard output will show a message like this while the code is running:

    ```
    ⠧ Doing something cool...
    ```

    And if the code succeeds you will see a message like this:
    ```
    ✔ Doing something cool [4.03 s]
    ```

    Or if it fails, you will see a similar message but with an "x" and the details of the exception will print on a new line.

    Please notice how the trailing dots at the end are automatically added. Also, I recommend capitalizing the first letter of the task name and proper nouns only, but the code does not enforce this.

### inputs.py
The file `system/inputs.py` contains tools for getting user input in a more secure way, such as masked inputs (like passwords). This is an alternative to using the `getpass` module, which works well, but isn't as flexible. The functions you can use are:

1. **get_masked_input(prompt: str) -> str**

    This function prompts the user for input and masks the input characters (like a password field). It returns the input as a string.

    Example usage:
    ```python
    from system.inputs import get_masked_input

    password = get_masked_input("Enter your password: ")
    ```

## The "apis" Folder
The file `apis/onepw.py` contains tools for interacting with various APIs, such as the OnePassword API. The classes you can use are:

1. **OnePasswordFetcher**

    This class provides methods to fetch sensitive information from 1Password items, such as API keys or credentials. It uses the `subprocess` module to call the 1Password CLI and retrieve item details in JSON format.

    Example usage:
    ```python
    from apis.onepw import OnePasswordFetcher

    fetcher = OnePasswordFetcher()
    api_key = fetcher.get_openai_api_key()
    ```

    Please note that this class requires the 1Password CLI to be installed and configured on your system. It also assumes you have an item in your 1Password vault with the title "OpenAI API Key" and a field named "API Key".

    The `get_openai_api_key` method is specifically designed to fetch the OpenAI API key from 1Password. If your item or field names differ, you will need to modify the method accordingly.

## The "apple_script" Folder
The file `apple_script/dialogues.py` contains tools for interacting with AppleScript dialogues with a more pythonic interface. The functions and classes you can use are:

1. **run_applescript(script: str) -> str**

    This function runs an AppleScript command and returns the output as a string. It uses the `subprocess` module to execute the AppleScript code.

    Example usage:
    ```python
    from apple_script.dialogues import run_applescript

    output = run_applescript('display dialog "Hello, world!"')
    print(output)
    ```

    If the AppleScript execution fails, a `RuntimeError` is raised with the error details.

2. **AppleScriptDialogues**

    This class provides methods to handle AppleScript dialogues for user interaction. The methods available are:

    - **ask_for_input(prompt: str, allow_cancel: bool = False) -> str | None**

        Displays a dialogue box asking the user for input. The user can optionally cancel the dialogue if `allow_cancel` is set to `True`.

        Example usage:
        ```python
        from apple_script.dialogues import AppleScriptDialogues

        user_input = AppleScriptDialogues.ask_for_input("Enter your name:", allow_cancel=True)
        if user_input is None:
            print("User cancelled the input.")
        else:
            print(f"User entered: {user_input}")
        ```

        Please note it's possible for the method to return an empty string if the user submits the dialogue without entering any text. This is different from cancelling the dialogue, which returns `None`.

    - **show_message(message: str, allow_cancel: bool = False) -> bool**

        Displays a message to the user in a dialogue box. The user can optionally cancel the dialogue if `allow_cancel` is set to `True`.

        Example usage:
        ```python
        from apple_script.dialogues import AppleScriptDialogues

        success = AppleScriptDialogues.show_message("Operation completed successfully.", allow_cancel=True)
        if success:
            print("User acknowledged the message.")
        else:
            print("User cancelled the message.")
        ```

        Returns `True` if the user clicked "OK" or the primary button, and `False` if they clicked "Cancel" (if allowed). If the AppleScript execution fails, a `RuntimeError` is raised.

## The "audio" Folder

### compiled_audio_driver.py

The file `audio/compiled_audio_driver.py` contains the `CompiledAudioDriver` class, which provides tools for processing and playing audio clips. This includes trimming silences, adjusting playback speed, and concatenating multiple audio clips into a single audio file. The class also supports adding silent delays between clips.

#### `CompiledAudioDriver`

This class allows you to collect multiple audio clips, process them (e.g., trim silences, adjust speed, preserve pitch), and compile them into one continuous audio file for playback.

##### Methods:

1. **`add_clip(file_path: str, speed: float = 1.3, silence_thresh: int = -43, min_silence_len: int = 1, preserve_pitch: bool = True)`**

    Adds an audio clip to the collection after processing it.

    - `file_path`: Path to the audio file.
    - `speed`: Playback speed multiplier (default is 1.3).
    - `silence_thresh`: dBFS threshold for silence trimming (default is -43).
    - `min_silence_len`: Minimum silence length in milliseconds to trim (default is 1 ms).
    - `preserve_pitch`: If `True`, preserves the original pitch when adjusting speed.

    Example usage:
    ```python
    from audio.compiled_audio_driver import CompiledAudioDriver

    driver = CompiledAudioDriver()
    driver.add_clip("example.mp3", speed=1.5, silence_thresh=-40, min_silence_len=500, preserve_pitch=True)
    ```

2. **`add_delay(seconds: float)`**

    Adds a silent audio segment of the specified duration to the collection.

    - `seconds`: Duration of silence in seconds.

    Example usage:
    ```python
    driver.add_delay(2.5)  # Adds 2.5 seconds of silence
    ```

3. **`compile()`**

    Concatenates all stored audio clips into one continuous audio file and saves it as WAV bytes.

    Example usage:
    ```python
    driver.compile()
    ```

4. **`play_compiled_audio()`**

    Plays the compiled audio. Make sure to call `compile()` first.

    Example usage:
    ```python
    driver.play_compiled_audio()
    ```