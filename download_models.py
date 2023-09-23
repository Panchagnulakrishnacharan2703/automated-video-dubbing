#!/bin/env python3
import os
import tempfile
import requests
import zipfile


def download_file_and_extract(url, extract_dir):
    with requests.get(url, stream=True) as r:
        file_size_bytes = int(r.headers.get("content-length", 0))
        chunk_size = 8192
        r.raise_for_status()
        print(f"Download started for {url} of size {file_size_bytes/1e9:.2f} Gb")

        with tempfile.NamedTemporaryFile() as tmp:
            for chunk in r.iter_content(chunk_size=8192):
                # add a progress bar!
                tmp.write(chunk)

            # it's still open!
            # unzip it to the destination here! replace me!
            print(tmp.name)


# this goes under models/
#wget https://indictrans2-public.objectstore.e2enetworks.net/it2_preprint_ckpts/en-indic-preprint.zip # be wary adventurer! It's 12.7 gigs!
#  unzip under models/ so it becomes something like models/en-indic-preprint

#download_file_and_extract("https://indictrans2-public.objectstore.e2enetworks.net/it2_preprint_ckpts/en-indic-preprint.zip")
download_file_and_extract("https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/as.zip", "")

# unzip all under models/v1/
# so it will become something like models/v1/<lang>
# wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/as.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/bn.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/brx.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/en+hi.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/en.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/gu.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/kn.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/ml.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/mni.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/mr.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/mr.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/pa.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/raj.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/ta.zip
#  wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/te.zip

