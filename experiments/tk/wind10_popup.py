import tkinter as tk
from pyob import NSScreen

def get_visible_screen_size():
    screen = NSScreen.mainScreen()
    visible_frame = screen.visibleFrame()
    x = int(visible_frame.origin.x)
    y = int(visible_frame.origin.y)
    width = int(visible_frame.size.width)
    height = int(visible_frame.size.height)
    return x, y, width, height

def create_popup():
    root = tk.Tk()
    root.title("Floating macOS Popup")
    root.attributes("-topmost", True)
    root.lift()

    x, y, width, height = get_visible_screen_size()
    # Convert from bottom-left macOS origin to Tk's top-left origin
    screen_height = root.winfo_screenheight()
    tk_y = screen_height - y - height

    root.geometry(f"{width}x{height}+{x}+{tk_y}")

    # UI
    frame = tk.Frame(root, bg="black")
    frame.pack(fill="both", expand=True)
    label = tk.Label(frame, text="macOS Floating Popup", fg="white", bg="black", font=("Helvetica", 24))
    label.pack(expand=True)

    root.mainloop()

create_popup()