#!/bin/bash

# Check if an input file was provided
if [ -z "$1" ]; then
    echo "Usage: ./extract_audio.sh <input_video_file>"
    exit 1
fi

INPUT_FILE="$1"
# Get filename without extension
FILENAME="${INPUT_FILE%.*}"
OUTPUT_FILE="${FILENAME}_audio.wav"

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it (e.g., brew install ffmpeg or sudo apt install ffmpeg)."
    exit 1
fi

echo "Extracting audio from: $INPUT_FILE"

# ffmpeg flags explained:
# -i: Input file
# -vn: Disable video recording (extract audio only)
# -acodec pcm_s16le: Uncompressed 16-bit PCM (standard WAV)
# -ar 16000: Set sampling rate to 16000 Hz (required for Whisper)
# -ac 1: Set to 1 channel (mono)
# -y: Overwrite output file if it exists

ffmpeg -i "$INPUT_FILE" -vn -acodec pcm_s16le -ar 16000 -ac 1 -y "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Success! Audio saved to: $OUTPUT_FILE"
else
    echo "Error: Extraction failed."
    exit 1
fi