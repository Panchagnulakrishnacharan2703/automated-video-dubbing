#!/bin/env python3
import os
import sys
import tempfile
import threading
import requests
import zipfile
from string import Template
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def download_file_and_extract(url, output_dir, task_id=0):
    """Download and extract zip file at url, to output_dir."""
    """The task_id is used for managing the progress bar during multi-threading
       so, make sure that it's unique."""
    file_name = url.split('/')[-1]
    chunk_size = 1024*1024
    with requests.get(url, stream=True) as r:
        file_size_bytes = int(r.headers.get("content-length", 0))
        chunks = file_size_bytes // chunk_size
        r.raise_for_status()

        with tempfile.NamedTemporaryFile() as tmp:
            desc = f"Downloading {file_name}"
            with tqdm(total=chunks, unit="MB", bar_format="{l_bar}{bar}| {n_fmt}{unit}/{total_fmt}{unit} [{remaining}]",
                      ncols=100, position=task_id, leave=None, desc=desc) as dl_progress:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    tmp.write(chunk)
                    dl_progress.update(1)

            with zipfile.ZipFile(tmp.name, "r") as temp_zip:
                temp_zip.extractall(output_dir)

    return f"Successfully extracted contents of {file_name} under {output_dir}{file_name.split('.')[0]}."


tts_base_url = Template("https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/$lang.zip")
tts_langs = ["as", "bn", "brx", "en+hi", "en", "gu", "hi", "kn", "ml", "mni", "mr", "or", "pa", "raj", "ta", "te"]
output_tts_base_dir = os.path.join(os.getcwd(), "models/v1/")


urls_outdir = [(tts_base_url.substitute(lang=lang), output_tts_base_dir) for lang in tts_langs]
urls_outdir.append(("https://indictrans2-public.objectstore.e2enetworks.net/it2_preprint_ckpts/en-indic-preprint.zip",
                    os.path.join(os.getcwd(), "models/")))

with ThreadPoolExecutor(max_workers=4) as executor:
    tasks = [executor.submit(download_file_and_extract, *(url, outdir, i))
             for i, (url, outdir) in enumerate(urls_outdir)]

    for task in as_completed(tasks):
        print(task.result())

print("Downloaded and extracted all the models! Cheers!")
