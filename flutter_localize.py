from typing import *
from openai import OpenAI
import os
import json
import argparse
from constants import LOCALE_TO_LANG

def read_input_file(file_path: str) -> str:
    file_content = ""
    with open(file_path, 'r') as file:
        file_content = file.read()
    # data = json.loads(file_content)
    # print(data)
    return file_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="flutter_l10n" , description="Localize a flutter file to target languages.")
    parser.add_argument('-i', '--file', type=str, help="Path to the input flutter template file.")
    parser.add_argument('-l', '--languages', nargs='+', type=list, help="The list of target languages.")
    parser.add_argument('-k', '--key', type=str, required=True, help="Your OpenAI API key.")
    parser.add_argument('-c', '--chunk', type=int, required=False, help="Number of messages per request.")

    args = parser.parse_args()

    file_path = args.file
    languages = ["".join(locale) for locale in args.languages]
    
    chunk = args.chunk
    api_key = args.key

    for lang in languages:
        if lang not in LOCALE_TO_LANG:
            raise KeyError()
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": f"system", "content": f"Translate this Resource Bundle file, an English template for localizing the Flutter application, into {LOCALE_TO_LANG[lang]}. Translate only the message value, use the description in message meta data for added context. Output a JSON file in target language."},
                {"role": "user", "content": read_input_file(file_path)}
            ]
        )

        out_file_path = f'out/app_{lang}.arb'
        directory = os.path.dirname(out_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(out_file_path, 'w') as file:
            file.write(completion.choices[0].message.content)
