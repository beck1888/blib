# Beck's Python Junk Drawer

Hi, and welcome to my "junk drawer" for my python code. In writing code over the years, I've amassed quite the collection of code I find myself using all the time. I've decided to lump it all into one standard "library" of sorts that I can quickly dump into my own projects.

This codebase has tools for many very different jobs, so I've tried to document what does what.

Also, I did use AI to help me clean up a lot of this code so other people can understand it. Just felt like I should mention that.

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