import tkinter as tk
import subprocess
import platform

def elevate_window_priority(root):
    # Use AppleScript to elevate the window's level to floating (above all other apps)
    script = f'''
    tell application "System Events"
        set frontmost of the first process whose unix id is {root.winfo_id()} to true
    end tell

    tell application "System Events"
        set theApp to first application process whose unix id is {root.winfo_id()}
        set the frontmost of theApp to true
    end tell
    '''
    subprocess.run(['osascript', '-e', script])

def create_popup():
    root = tk.Tk()
    root.title("Priority Popup")
    root.geometry("400x200")
    root.attributes("-topmost", True)  # Tkinter level
    root.lift()  # Bring window to top in stacking order

    # macOS-specific: force window to be key and frontmost (in a non-fullscreen way)
    if platform.system() == "Darwin":
        root.after(100, lambda: elevate_window_priority(root))

    label = tk.Label(root, text="This is a macOS priority popup!", font=("Helvetica", 16))
    label.pack(expand=True)

    root.mainloop()

create_popup()