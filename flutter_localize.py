import collections
import os
import json
import argparse
from typing import *
from openai import OpenAI
from constants import LOCALE_TO_LANG

def read_input_file(file_path: str) -> str:
    file_content = ""
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="flutter_l10n" , description="Localize a flutter file to target languages.")
    parser.add_argument('-i', '--file', type=str, help="Path to the input flutter template file.")
    parser.add_argument('-l', '--languages', nargs='+', type=list, help="The list of target languages.")
    parser.add_argument('-k', '--key', type=str, required=True, help="Your OpenAI API key.")
    parser.add_argument('-c', '--chunk', type=int, required=False, help="Number of messages per API request.")

    args = parser.parse_args()

    file_path = args.file
    languages = ["".join(locale) for locale in args.languages]
    chunk = args.chunk if args.chunk else 5
    api_key = args.key

    directory = "out"
    if not os.path.exists(directory):
            os.makedirs(directory)
    
    # parse the JSON/ARB file, for Flutter framework
    jsonData = json.loads(read_input_file(file_path), object_pairs_hook=collections.OrderedDict)
    messages = []
    messageMeta = {}
    # message with meta, message without meta, meta without message
    for k in jsonData.keys():
        if not k.startswith('@'):
            messages.append(k)
            messageMeta[k] = jsonData['@'+k] if '@'+k in jsonData else None
    
    client = OpenAI()

    for lang in languages:
        if lang not in LOCALE_TO_LANG:
            raise KeyError()
        
        result = []

        for message in messages:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": f"system", "content": f"Translate the following messages from an Application Resource Bundle (ARB) file into {LOCALE_TO_LANG[lang]}.\n\
                                                    Context: These JSON key-value pairs are from a Flutter application's localization template.\n\
                                                    Instructions:\n\
                                                    1. Only translate the message value.\n\
                                                    2. Out put keys and values should be a string type in double quotation mark.\n\
                                                    3. Use the provided context for more accurate translations.\n\
                                                    4. Output each JSON key-value pair without leading or tailing brackets, commas, spaces, or line change."
                    },
                    {"role": "user", "content": f'"{message}": "{jsonData[message]}"\n\
                                                {"Its usage context being: " + messageMeta[message]["description"] if message in messageMeta and messageMeta[message]["description"] else ""}'
                    }
                ]
            )
            result.append(completion.choices[0].message.content)

        out_file_path = f'{directory}/app_{lang}.arb'
        with open(out_file_path, 'w') as file:
            file.write("{\n"+",\n".join(result)+"\n}")

