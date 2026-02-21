#!/usr/bin/env python3
import sys
import os
from faster_whisper import WhisperModel

def format_timestamp(seconds: float):
    """Converts seconds to SRT time format: HH:MM:SS,mmm"""
    milliseconds = int(round((seconds - int(seconds)) * 1000))
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def transcribe_to_srt(audio_path):
    output_path = os.path.splitext(audio_path)[0] + ".srt"
    
    # Initialize model
    # Use device="cpu" if you don't have an NVIDIA GPU
    print("Loading AI model (medium)...")
    model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)

    print(f"Transcribing: {audio_path}")
    # vad_filter=True is crucial for old movies to ignore non-speech noise
    segments, info = model.transcribe(audio_path, beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))

    print(f"Segments: {segments}")
    print(f"All information: {info}")
    
    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

    with open(output_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{segment.text.strip()}\n\n")
            
            # Print progress to console
            print(f"[{start}] {segment.text.strip()}")

    print(f"\nDone! Subtitles saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run transcribe.py <path_to_audio.wav>")
        sys.exit(1)
    
    transcribe_to_srt(sys.argv[1])