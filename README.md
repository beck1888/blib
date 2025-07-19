## Beck’s Python Junk Drawer

A grab‑bag “standard library” of handy Python utilities I’ve collected (and often refactored with AI) over the years. Designed for quick copy‑&‑paste into your own projects.

> **Platform & prerequisites**
> • **macOS only.** Untested elsewhere.
> • Some tools assume you’ve installed and configured:
>   • 1Password CLI (`op`)
>   • Your own API keys (e.g. OpenAI)

---

### 📂 system

#### **`terminal.py`**

Tools for fancier CLI interactions—spinners, cursor control, and richer text.

* **`Cursor`**

  * `show()` ▸ unhide the terminal cursor
  * `hide()` ▸ hide the terminal cursor

* **`Spinner`**
  A context‑manager spinner (like npm’s) that auto‑handles cursor state, timing, and success/failure indicators.

  ```python
  from system.terminal import Spinner

  with Spinner("Building project"):
      build_project()
  ```

  * **Running:**

    ```
    ⠧ Building project...
    ```
  * **On success:**

    ```
    ✔ Building project [2.15 s]
    ```
  * **On error:**

    ```
    ✖ Building project [2.15 s]
    Traceback (most recent call last):
    ...
    ```

---

#### **`inputs.py`**

Secure, flexible masked input (password‑style).

* **`get_masked_input(prompt: str = "Password: ") -> str`**
  Reads input from the user, displaying a mask character instead of each keystroke.

  ```python
  from system.inputs import get_masked_input

  pwd = get_masked_input("Enter API password: ")
  ```

---

### 📂 apis

#### **`onepw.py`**

Fetch secrets from 1Password via its CLI.

* **`OnePasswordFetcher`**

  ```python
  from apis.onepw import OnePasswordFetcher

  fetcher = OnePasswordFetcher()
  key = fetcher.get_openai_api_key()
  ```

  * **Dependencies:** 1Password CLI installed & signed in
  * **Defaults:** looks for an item named `"OpenAI API Key"` with a field labelled `"API Key"`.
  * **Customizing:** override item name or field label in the method call.

---

### 📂 apple\_script

#### **`dialogues.py`**

Python wrappers around AppleScript dialogs.

* **`run_applescript(script: str) -> str`**
  Execute raw AppleScript and return its output (or raise `RuntimeError` on failure).

* **`AppleScriptDialogues`**

  * `ask_for_input(prompt: str, allow_cancel: bool = False) -> str | None`
    Show an input dialog; returns the text or `None` if cancelled.
  * `show_message(message: str, allow_cancel: bool = False) -> bool`
    Show an alert; returns `True` if “OK” clicked, `False` if cancelled.

  ```python
  from apple_script.dialogues import AppleScriptDialogues

  name = AppleScriptDialogues.ask_for_input("Your name:", allow_cancel=True)
  if name is None:
      print("Cancelled")
  else:
      AppleScriptDialogues.show_message(f"Hello, {name}!")
  ```

---

### 📂 audio

#### **`compiled_audio_driver.py`**

Collect, process, and stitch together audio clips (trimming silence, changing speed, preserving pitch) plus optional silent gaps.

* **`CompiledAudioDriver`**

  1. `add_clip(file_path: str, speed: float = 1.3, silence_thresh: int = -43, min_silence_len: int = 1, preserve_pitch: bool = True)`
     Queue an audio file for processing.
  2. `add_delay(seconds: float)`
     Insert silence of given length (in seconds).
  3. `compile() -> bytes`
     Process all clips + delays into one WAV buffer.
  4. `play_compiled_audio()`
     Play back the compiled track (after `compile()`).

  ```python
  from audio.compiled_audio_driver import CompiledAudioDriver

  driver = CompiledAudioDriver()
  driver.add_clip("intro.mp3", speed=1.5)
  driver.add_delay(2.0)
  driver.add_clip("outro.mp3", speed=1.0)
  driver.compile()
  driver.play_compiled_audio()
  ```
