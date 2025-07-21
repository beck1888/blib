"""
tones.py

Provides utility functions to generate and save audio tones as .wav files.

This module contains:
- generate_sine_wave: Generates a sine wave signal as a numpy array.
- save_wave: Saves a numpy array as a .wav file.
"""

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

    Args:
        frequency (float): Frequency of the sine wave in Hz.
        duration (float): Duration of the sine wave in seconds.
        amplitude (float, optional): Amplitude of the sine wave, ranging from 0.0 to 1.0. Defaults to 0.5.
        sample_rate (int, optional): Number of samples per second. Defaults to 44100.

    Returns:
        np.ndarray: Array of sine wave samples.
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

    Args:
        file_path (str): Path to save the .wav file (relative or absolute).
        wave (np.ndarray): Array of audio samples to save.
        sample_rate (int, optional): Number of samples per second. Defaults to 44100.

    Raises:
        FileNotFoundError: If the directory cannot be created.
        ValueError: If the wave array is invalid.

    """
    # Normalize to 16-bit PCM range
    wave_int16 = np.int16(wave * 32767)

    # Create target directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    # Save
    write(file_path, sample_rate, wave_int16)
    print(f"✔ Saved: {file_path}")