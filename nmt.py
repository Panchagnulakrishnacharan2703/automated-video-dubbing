#!/bin/env python
import argparse
from inference.engine import Model
import os
import sys

model_subdirs = {
    "ct2-int8": "ct2_int8_model",
    "ct2-fp16": "ct2_fp16_model",
    "fairseq": "fairseq_model"
}

model_types = {
    "ct2-int8": "ctranslate2",
    "ct2-fp16": "ctranslate2",
    "fairseq": "fairseq"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text from English to output language.")
    parser.add_argument("--input-file",
                        help="Input file containing English text", required=True)
    parser.add_argument("--output-file",
                        help="Output file to write translated text. \
                        If it is not given, then the result will be written to standard output.")
    parser.add_argument("--target", help="Target language", required=True)
    parser.add_argument("--model", choices=("ct2-int8", "ct2-f16", "fairseq"),
                        help="Model to use.", required=True)
    parser.add_argument("--model-dir",
                        help="Path to the root of the unzipped archive of the models.", required=True)
    parser.add_argument("--use-cuda",
                        help="Use cuda. Add flag if you have a CUDA-compliant graphics card. Otherwise omit it.", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.model_dir):
        print(f"{args.model_dir} does not exist. Check the path. Aborting.", file=sys.stderr)
        exit(1)

    print(args)
    model_path = os.path.join(args.model_dir, model_subdirs[args.model])
    model = Model(model_path, model_type=model_types[args.model],
                  device="cuda" if args.use_cuda else "cpu")

    # TODO: Do something for multiple paragraphs, if that's required!
    with open(args.input_file, "r") as file:
        para = file.readlines()

    # TODO: there is translate paragraphs, too! Could use that?
    result = model.translate_paragraph(para[0], "eng_Latn", args.target)

    if args.output_file:
        try:
            with open(args.output_file, "w") as file:
                file.write(result)
            print(f"Wrote output to { args.output_file }")
        except:
            print("Failed to write to file.")
            exit(2)
    else:
        print(result)
