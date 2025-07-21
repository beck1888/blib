raise NotImplementedError("This code is still a work in progress and often segfaults. Use at your own risk.")

import os
import threading
import time
from pydub import AudioSegment
import simpleaudio as sa

SUPPORTED_FILE_TYPES: tuple[str, ...] = ('mp3', 'wav')

class OOPAudio:
    def __init__(self, audio_file_path: str):
        # Current playback position in ms
        self.position: float = 0.0  
        # Threading & control
        self._play_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._play_obj = None
        self._loop = False
        self._block = False
        self._start_time = 0.0

        # Validate file
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Invalid file path: {audio_file_path}")
        ext = audio_file_path.rsplit('.', 1)[-1].lower()
        if ext not in SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"Invalid file type. Got '{ext}' but only {SUPPORTED_FILE_TYPES} are supported."
            )

        # Load audio
        self.audio = AudioSegment.from_file(audio_file_path)

    def fire(self, block_script_execution: bool = False):
        """
        Plays the full sound once (from start to finish),
        optionally blocking until done.
        """
        seg = self.audio
        play_obj = sa.play_buffer(seg.raw_data, seg.channels, seg.sample_width, seg.frame_rate)
        if block_script_execution:
            play_obj.wait_done()

    def advanced_driver_play(self, block_script_execution: bool = False, loop: bool = False):
        """
        Starts (or restarts) playback from self.position in a background thread.
        Can only have one advanced play at a time. Set loop=True to repeat.
        """
        # Stop any existing play
        self.advanced_driver_pause()

        # Store mode
        self._loop = loop
        self._block = block_script_execution
        self._stop_event.clear()

        def _runner():
            while not self._stop_event.is_set():
                seg = self.audio[self.position:]
                self._start_time = time.time()
                self._play_obj = sa.play_buffer(seg.raw_data, seg.channels, seg.sample_width, seg.frame_rate)

                if self._block:
                    self._play_obj.wait_done()
                else:
                    # Poll until done or stopped
                    while self._play_obj.is_playing() and not self._stop_event.is_set():
                        time.sleep(0.05)
                    if self._stop_event.is_set():
                        self._play_obj.stop()

                # If looping, reset position; else break
                if loop and not self._stop_event.is_set():
                    self.position = 0.0
                    continue
                break

        self._play_thread = threading.Thread(target=_runner, daemon=True)
        self._play_thread.start()
        if block_script_execution:
            self._play_thread.join()

    def advanced_driver_pause(self):
        """
        Pauses playback, stopping the thread and remembering how far we got.
        """
        if self._play_obj and self._play_obj.is_playing():
            # Signal thread to stop
            self._stop_event.set()
            # Stop audio immediately
            self._play_obj.stop()
            # Calculate elapsed ms
            elapsed = (time.time() - self._start_time) * 1000.0
            self.position += elapsed
            # Clamp
            self.position = min(self.position, len(self.audio))
            # Wait for thread exit
            if self._play_thread:
                self._play_thread.join()

    def advanced_driver_seek(self, position: float):
        """
        Move to `position` milliseconds into the audio.
        If currently playing, restarts playback from the new position.
        """
        if not (0 <= position <= len(self.audio)):
            raise ValueError(f"Position {position}ms out of range (0–{len(self.audio)}ms)")
        # Update position
        self.position = position
        # If playing, restart
        if self._play_thread and self._play_thread.is_alive():
            self.advanced_driver_play(self._block, self._loop)