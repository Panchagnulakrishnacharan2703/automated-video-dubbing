#!/bin/env python3
import io
from TTS.utils.synthesizer import Synthesizer
from src.inference import TextToSpeechEngine
from scipy.io.wavfile import write as scipy_wav_write
import argparse

parser = argparse.ArgumentParser(description="Apply TTS on the input audio file, and generate an output audio file.")
parser.add_argument("--input", "-i", help="Input text file", required=True)
parser.add_argument("--lang", help="Language of the source text, and the audio output.", required=True)
parser.add_argument("--speaker", help="Speaker, male or female.", choices=("male", "female"), default="male")
parser.add_argument("--sampling_rate", type=int, help="Sampling rate, default is 18000.", default=18000)
parser.add_argument("--output", "-o", help="File to write the output to", default="output_tts.wav")
args = parser.parse_args()


default_sampling_rate = args.sampling_rate
lang = args.lang
speaker = args.speaker

# TODO: good enough for this, for something more robust, do the audio in chunks and merge them
#       Looks like it's split into sentences anyway. Keep that in mind when doing the full thing!
with open(args.input, "r", encoding="utf-8") as file:
    text = "".join(file.readlines()) 


model  = Synthesizer(
    tts_checkpoint=f'models/v1/{lang}/fastpitch/best_model.pth',
    tts_config_path=f'models/v1/{lang}/fastpitch/config.json',
    tts_speakers_file=f'models/v1/{lang}/fastpitch/speakers.pth',
    # tts_speakers_file=None,
    tts_languages_file=None,
    vocoder_checkpoint=f'models/v1/{lang}/hifigan/best_model.pth',
    vocoder_config=f'models/v1/{lang}/hifigan/config.json',
    encoder_checkpoint="",
    encoder_config="",
    use_cuda=False,
)

# Setup TTS Engine

models = {
    lang: model,
}
engine = TextToSpeechEngine(models)

raw_audio = engine.infer_from_text(
    input_text=text,
    lang=lang,
    speaker_name=speaker
)

byte_io = io.BytesIO()
scipy_wav_write(byte_io, default_sampling_rate, raw_audio)

with open(args.output, "wb") as f:
    f.write(byte_io.read())
