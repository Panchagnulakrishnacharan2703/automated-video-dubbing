#!/bin/env python3
import whisper
import time
import os.path
import argparse

# TODO: Could I output this with JSON? With timestamps!

start = time.perf_counter()
model = whisper.load_model("base")
parser = argparse.ArgumentParser(description="Generate the text from an input (English) audio file.")
parser.add_argument("--input", "-i", help="Input audio file", required=True)
parser.add_argument("--output", "-o", help="File to write the transcription to")
# parser.add_argument("--gen-subs", help="Generate a subtitle file to subs.vtt")

args = parser.parse_args()

# TODO: Check extension as well
# TODO: Make these functions to be imported, and put all this into name==__main__ block
if not os.path.isfile(args.input):
    print(f"Not valid audio file: {args.input}.")
    exit(1)

if not args.input.endswith((".mp3", ".ogg", ".mp4")):
    print(f"Not an audio file: {args.input}.")
    exit(2)


result = model.transcribe(args.input)
end = time.perf_counter()

if args.output:
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result["text"])
else:
    print(result["text"])

# creating the subtitles
print(result["segments"])  # Each sentence is in a dictionary with the relevant data being at keys id, start, end, text

print(f'ASR completed in {end - start:0.4f}s')
