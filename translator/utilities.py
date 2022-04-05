import contextlib
import wave


def get_chunks(text: str, maxlength: int):
    start = 0
    end = 0
    while start + maxlength < len(text) and end != -1:
        end = text.rfind(" ", start, start + maxlength + 1)
        yield text[start:end]
        start = end + 1
    yield text[start:]


def get_audio_duration(audio_file):
    """Determine the length of the audio file."""
    with contextlib.closing(wave.open(audio_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
