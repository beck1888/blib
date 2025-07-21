import numpy as np
from scipy.io.wavfile import write
import os

def generate_sine_wave(
    frequency: float,
    duration: float,
    amplitude: float = 0.5,
    sample_rate: int = 44100
) -> np.ndarray:
    """
    Generates a sine wave signal.

    :param frequency: Frequency in Hz
    :param duration: Duration in seconds
    :param amplitude: Amplitude from 0.0 to 1.0
    :param sample_rate: Samples per second
    :return: Numpy array of sine wave samples
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def save_wave(
    file_path: str,
    wave: np.ndarray,
    sample_rate: int = 44100
):
    """
    Saves a wave array to a .wav file.

    :param file_path: Relative or absolute file path
    :param wave: Numpy array of samples
    :param sample_rate: Samples per second
    """
    # Normalize to 16-bit PCM range
    wave_int16 = np.int16(wave * 32767)

    # Create target directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    # Save
    write(file_path, sample_rate, wave_int16)
    print(f"✔ Saved: {file_path}")