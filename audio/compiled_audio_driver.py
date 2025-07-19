import io
from pydub import AudioSegment, silence
from pydub.playback import play
from pydub.effects import speedup
import os
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
        self._clip_bytes = []          # List of processed clips as WAV bytes
        self.compiled_audio_bytes = None  # Compiled full audio as WAV bytes

    def add_clip(
        self,
        file_path: str,
        speed: float = DEFAULT_SPEED,
        silence_thresh: int = DEFAULT_SILENCE_THRESH,
        min_silence_len: int = DEFAULT_MIN_SILENCE_LEN,
        preserve_pitch: bool = DEFAULT_PRESERVE_PITCH,
    ):
        """
        Load an audio file, trim silences, adjust speed (with optional
        pitch preservation), then store as WAV bytes.

        :param file_path: Path to the audio file.
        :param speed: Playback speed multiplier (1.0 = original).
        :param silence_thresh: dBFS threshold for silence trimming.
        :param min_silence_len: Minimum silence length (ms) to trim.
        :param preserve_pitch: If True, keep original pitch when speeding.
        """
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
        print(f"added clip in {elapsed_time * 1000:.2f} milliseconds")

    def add_delay(self, seconds: float):
        """
        Add a silent audio segment of the specified duration.
        
        :param seconds: Duration of silence in seconds.
        """
        # Create silent audio segment
        silence_duration_ms = int(seconds * 1000)  # Convert to milliseconds
        silent_segment = AudioSegment.silent(duration=silence_duration_ms)
        
        # Export to WAV in memory
        buf = io.BytesIO()
        silent_segment.export(buf, format="wav")
        self._clip_bytes.append(buf.getvalue())
        
        print(f"added {seconds} second delay")

    def compile(self):
        """
        Concatenate all stored clips into one AudioSegment,
        export as WAV bytes, and save to compiled_audio_bytes.
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
        print(f"compiled audio in {elapsed_time * 1000:.2f} milliseconds")

    def play_compiled_audio(self):
        """
        Play the compiled audio. Call compile() first.
        """
        if not self.compiled_audio_bytes:
            raise RuntimeError("No compiled audio: call compile() first.")

        buf = io.BytesIO(self.compiled_audio_bytes)
        segment = AudioSegment.from_file(buf, format="wav")
        play(segment)