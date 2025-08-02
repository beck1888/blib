import os
from compiled_audio_driver import CompiledAudioDriver

def get_numeric_audio_tokens(dir_path="/audio/resources/num_audios"):
    audio_files = os.listdir(dir_path)
    tokens = []

    for f in audio_files:
        name, ext = os.path.splitext(f)
        if ext == ".mp3" and name.isdigit():
            tokens.append(int(name))

    return sorted(tokens, reverse=True)

def decompose_number(n, tokens):
    result = []
    for token in tokens:
        while n >= token:
            n -= token
            result.append(f"{token}.mp3")
        if n == 0:
            break
    return result

def get_audio_files(n, dir_path="audio/resources/num_audios"):
    if not isinstance(n, int):
        raise ValueError("Only integer numbers are supported.")

    if n >= 10_000:
        raise ValueError('Max number is 9,999.')
    
    if n == 0:
        raise ValueError('Zero not supported.')
    
    if n < 0:
        raise ValueError("Number must be positive.")
    
    tokens = get_numeric_audio_tokens(dir_path)
    return decompose_number(n, tokens)

def main():
    n = int(input("Enter a number to play using audio files: ").strip())
    clips = get_audio_files(n)
    audio = CompiledAudioDriver()
    for clip in clips:
        audio.add_clip(f"audio/resources/num_audios/{clip}", speed=1.1)
    audio.play_compiled_audio()

if __name__ == "__main__":
    main()
