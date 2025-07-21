"""
compiled_audio_driver.py

Provides a class for easily making one audio file out of many.
"""

import io
from pydub import AudioSegment, silence
from pydub.playback import play
from pydub.effects import speedup
from time import time

# Defaults
DEFAULT_SILENCE_THRESH = -43   # dBFS (-40 is common; closer to zero = more aggressive)
DEFAULT_MIN_SILENCE_LEN = 1    # ms (500ms common; lower = more aggressive)
DEFAULT_SPEED = 1.3            # Normal speed is 1.0
DEFAULT_PRESERVE_PITCH = True # New default

class CompiledAudioDriver:
    """
    Collect multiple audio clips (with silence trimming, speed adjustment,
    and optional pitch preservation), store as raw bytes, compile into
    one continuous audio, and play.
    """

    def __init__(self):
        """
        Initializes the CompiledAudioDriver instance.

        Attributes:
            _clip_bytes (list): List of processed audio clips stored as WAV bytes.
            compiled_audio_bytes (bytes or None): The compiled audio as WAV bytes.
            needs_recompile (bool): Indicates if the audio needs recompilation.
        """
        self._clip_bytes = []             # List of processed clips as WAV bytes
        self.compiled_audio_bytes = None  # Compiled full audio as WAV bytes
        self.needs_recompile = True       # Track when file changes and needs to be compiled again

    def add_clip(
        self,
        file_path: str,
        speed: float = DEFAULT_SPEED,
        silence_thresh: int = DEFAULT_SILENCE_THRESH,
        min_silence_len: int = DEFAULT_MIN_SILENCE_LEN,
        preserve_pitch: bool = DEFAULT_PRESERVE_PITCH,
    ):
        """
        Adds an audio clip to the compilation after processing.

        Args:
            file_path (str): Path to the audio file.
            speed (float): Playback speed multiplier (1.0 = original speed).
            silence_thresh (int): dBFS threshold for silence trimming.
            min_silence_len (int): Minimum silence length (ms) to trim.
            preserve_pitch (bool): If True, preserves the original pitch when adjusting speed.
        """
        # Set needs recompile flag to on because a change is made
        self.needs_recompile = True

        # Timing
        start_time = time()

        # Load source
        audio = AudioSegment.from_file(file_path)

        # Trim silences
        chunks = silence.split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        trimmed = sum(chunks) if chunks else AudioSegment.empty()

        # Adjust speed
        if speed != 1.0:
            if preserve_pitch:
                # time-stretch without changing pitch
                trimmed = speedup(trimmed, playback_speed=speed)
            else:
                # change frame rate (alters pitch), then reset rate
                new_fr = int(trimmed.frame_rate * speed)
                trimmed = trimmed._spawn(trimmed.raw_data,
                                        overrides={'frame_rate': new_fr})
                trimmed = trimmed.set_frame_rate(audio.frame_rate)

        # Export to WAV in memory
        buf = io.BytesIO()
        trimmed.export(buf, format="wav")
        self._clip_bytes.append(buf.getvalue())

        # Log timing in ms
        elapsed_time = time() - start_time
        # print(f"added clip in {elapsed_time * 1000:.2f} milliseconds")

    def add_delay(self, seconds: float):
        """
        Adds a silent audio segment of the specified duration.

        Args:
            seconds (float): Duration of silence in seconds.
        """
        # Set needs recompile flag to on because a change is made
        self.needs_recompile = True

        # Create silent audio segment
        silence_duration_ms = int(seconds * 1000)  # Convert to milliseconds
        silent_segment = AudioSegment.silent(duration=silence_duration_ms)
        
        # Export to WAV in memory
        buf = io.BytesIO()
        silent_segment.export(buf, format="wav")
        self._clip_bytes.append(buf.getvalue())
        
        # print(f"added {seconds} second delay")

    def compile(self):
        """
        Concatenates all stored audio clips into one continuous audio segment.

        This method processes all stored clips, combines them, and saves the
        result as WAV bytes in `compiled_audio_bytes`. Marks the audio as compiled.
        """
        # Timing
        start_time = time()

        combined = AudioSegment.empty()
        for data in self._clip_bytes:
            buf = io.BytesIO(data)
            segment = AudioSegment.from_file(buf, format="wav")
            combined += segment

        buf = io.BytesIO()
        combined.export(buf, format="wav")
        self.compiled_audio_bytes = buf.getvalue()

        # Log timing in ms
        elapsed_time = time() - start_time
        # print(f"compiled audio in {elapsed_time * 1000:.2f} milliseconds")

        # Audio is considered compiled until changed
        self.needs_recompile = False

    def play_compiled_audio(self):
        """
        Plays the compiled audio.

        If the audio has been modified since the last compilation, it will
        automatically recompile before playback.
        """
        if self.needs_recompile:
            self.compile()

        buf = io.BytesIO(self.compiled_audio_bytes)
        segment = AudioSegment.from_file(buf, format="wav")
        play(segment)

    def save_compiled_audio(self, fp: str):
        """
        Saves the compiled audio to a specified file path.

        Args:
            fp (str): File path (relative or absolute) to save the compiled audio.

        Raises:
            RuntimeError: If the compiled audio is missing or not generated.
        """
        if self.needs_recompile:
            self.compile()

        with open(fp, "wb") as f:
            f.write(self.compiled_audio_bytes)
        # print(f"saved compiled audio to {fp}")