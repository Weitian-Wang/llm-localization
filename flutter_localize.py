import collections
import os
import json
import argparse
import base64
from tqdm import tqdm
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
    parser.add_argument('-s', '--screenshot', type=str, help="The folder that contains all of your screenshots.")
    parser.add_argument('-c', '--chunk', type=int, required=False, help="Number of messages per API request.")

    args = parser.parse_args()

    file_path = args.file
    languages = ["".join(locale) for locale in args.languages]
    api_key = args.key
    image_dir = args.screenshot
    chunk = args.chunk if args.chunk else 5

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
        print(f"Localizing input into {LOCALE_TO_LANG[lang]}")
        
        out_file_path = f'{directory}/app_{lang}.arb'
        with open(out_file_path, 'w') as file:
            file.write("{\n")
            for idx in tqdm(range(len(messages))):
                message = messages[idx]
                content = [
                    {
                        "type": "text", 
                        "text": f'"{message}": "{jsonData[message]}"\n\
                                {"Its usage context is: " + messageMeta[message]["description"] if message in messageMeta and messageMeta[message] and messageMeta[message]["description"] else ""}'
                    }
                ]
                for extension in [".png", ".jpeg", ".jpg"]:
                    detail = "low"
                    image_path = os.path.join(image_dir if image_dir else "", message+extension)
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as image_file:
                            content.append(
                                {
                                    "type": "image_url",
                                    "image_url": 
                                    {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}",
                                        "detail": "low"
                                    }
                                }
                            )
                # append image input if image flag is true
                completion = client.chat.completions.create(
                    # cheap and fast gpt-4 mode
                    # model="gpt-4o",
                    # gpt with image support
                    model="gpt-4-vision-preview",
                    messages=[
                        {"role": f"system", "content": f"Translate the following messages from an Application Resource Bundle (ARB) file into {LOCALE_TO_LANG[lang]}.\n\
                                                        These JSON key-value pairs are from a Flutter application's localization template.\n\
                                                        Instructions:\n\
                                                        1. Output each JSON key-value pair without leading or tailing brackets, commas, spaces, or line change.\n\
                                                        2. Like the inputs, the outcome key and value should be enclosed in double quotations.\n\
                                                        2. Use the provided context for more accurate translations.\n\
                                                        4. If the message contains markdown formatting syntax, keep those syntax.\n\
                                                        5. If screenshot of the widget is provided, use the it for extra context.\n\
                                                        6. The message is from a stress tracking app, make sure the message sounds caring and cute"
                        },
                        {
                            "role": "user", 
                            "content": content
                        }
                    ]
                )
                file.write('\t' + repr(completion.choices[0].message.content).strip('\'') + (',\n' if idx < len(messages) - 1 else ''))
            file.write("\n}")
