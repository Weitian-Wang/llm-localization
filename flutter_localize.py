from typing import *
from openai import OpenAI
import json
import argparse

LOCALE_TO_LANG = {
    "af": "Afrikaans",
    "am": "Amharic",
    "ar": "Arabic",
    "as": "Assamese",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali Bangla",
    "bs": "Bosnian",
    "ca": "Catalan Valencian",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Modern Greek",
    "en": "English",
    "es": "Spanish Castilian",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fi": " Filipino Pilipino",
    "fr": "French",
    "gl": "Galician",
    "gs": " Swiss German Alemannic Alsatian",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer Central Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ky": "Kirghiz Kyrgyz",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Burmese",
    "nb": "Norwegian Bokmål",
    "ne": "Nepali",
    "nl": "Dutch Flemish",
    "no": "Norwegian",
    "or": "Oriya",
    "pa": "Panjabi Punjabi",
    "pl": "Polish",
    "ps": "Pushto Pashto",
    "pt": "Portuguese",
    "ro": "Romanian Moldavian Moldovan",
    "ru": "Russian",
    "si": "Sinhala Sinhalese",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "zh": "Chinese",
    "zu": "Zulu",
}

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
    for lang in languages:
        if lang not in LOCALE_TO_LANG:
            raise KeyError()
    

    chunk = args.chunk
    api_key = args.key

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": f"system", "content": f"Translate this Resource Bundle file, an English template for localizing the Flutter application, into ${LOCALE_TO_LANG[languages[0]]}. Translate only the message value, use the description in message meta data for added context. Output a JSON file in target language."},
            {"role": "user", "content": read_input_file(file_path)}
        ]
    )
    
    print(completion.choices[0].message.content)
