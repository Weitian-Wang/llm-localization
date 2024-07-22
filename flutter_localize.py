import collections
import os
import json
import argparse
import base64
from tqdm import tqdm
from dotenv import load_dotenv
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
    parser.add_argument('-s', '--screenshot', type=str, help="The folder that contains all of your screenshots.")
    parser.add_argument('-c', '--chunk', type=int, required=False, help="Number of messages per API request.")

    args = parser.parse_args()

    file_path = args.file
    languages = ["".join(locale) for locale in args.languages]
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
    
    load_dotenv()
    client = OpenAI()

    for lang in languages:
        if lang not in LOCALE_TO_LANG:
            raise KeyError()
        print(f"Localizing {LOCALE_TO_LANG[lang]}")
        
        out_file_path = f'{directory}/app_{lang}.arb'
        with open(out_file_path, 'w') as file:
            file.write("{\n")
            for idx in tqdm(range(len(messages))):
                message = messages[idx]
                content = [
                    {
                        "type": "text",
                        "text": repr(f'"{message}":"{jsonData[message]}"').strip('\'')
                    }
                ]
                # content = f'"{message}":"{jsonData[message]}"'
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
                completion = client.chat.completions.create(
                    # cheap and fast gpt-4 mode
                    # model="gpt-4o",
                    # gpt with image support
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": [{
                                "type": "text",
                                "text": 
f"Translate the following key-value pair from a Flutter localization template file to {LOCALE_TO_LANG[lang]}.\n\
Instructions:\n\
1. Translate the value only and leave the key unchanged.\n\
2. Output JSON key-value pairs without leading or tailing brackets, commas, spaces, or line changes.\n\
3. Enclose the outcome key and value in double quotations, just like the input.\n\
4. Retain any markdown formatting syntax. Keep special character escapes. Preserve any control character backslashes.\n\
5. If a screenshot of the widget is provided, use it for extra context."
+ f'\n{"6. The message context from metadata is: " + messageMeta[message]["description"] if message in messageMeta and messageMeta[message] and messageMeta[message]["description"] else ""}'
                            }]
                        },
                        {
                            "role": "user", 
                            "content": content
                        }
                    ],
                    # make mode output more deterministic
                    temperature=0
                )

                file.write('\t' + completion.choices[0].message.content + (',\n' if idx < len(messages) - 1 else ''))
            file.write("\n}")



# '"iOSWidgetScreenStep2Title": "Step 2: \n Search for \'Furry\'"' - regular content