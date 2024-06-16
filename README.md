# LLM Localization Automation
Welcome to the LLM Localization project! This project aims to automate localization for Flutter applications using large language models (LLMs).

## Overview
LLM Localization is a script that simplifies the process of localizing apps. It leverages the power of large language models to automatically generate and manage translations for your app, ensuring that your app can reach a wide audience with ease. 

One of the project's primary objective is to enhance the translation fidelity beyond the traditional translation methods, by incorporating message descriptions and screenshots as additional contextual cues, thereby ensuring more accurate and contextually relevant translations.

## Features
- Automated Localization: Generate localization Application Bundle File for your Flutter app.
- Multi-language Support: Supports multiple languages, making your app accessible to a wider audience.
- Customization: Fine-tune translations to match the tone and style of your app.

## Getting Started
### Prerequisites
- Python version 3.9+
- [OpenAI API key](https://openai.com/api/)

### Installation
#### 1. Clone the repository
```sh
git clone https://github.com/Weitian-Wang/llm-localization.git
cd llm-localization
```

#### 2. Install dependencies
```sh
pip3 install -r requirements.txt
```

#### 3. Set up API key
`export` your API key as an environment variable
```sh
export OPENAI_API_KEY=your-api-key
```

### Usage
An exemplary usage is in `flutter_l10n` file. 
```sh
python3 flutter_localize.py -i app_en.arb -l es ja zh -k $OPENAI_API_KEY -s screenshots
```
Here's a breakdown of the parameters:
- `-i`, `--file` (str, required): Path to the input flutter template file.
- `-l`, `--languages` (list, required): The list of target languages.
- `-k`, `--key` (str, required): Your OpenAI API key.
- `-s`, `--screenshot` (str, optional): The folder that contains all of your screenshots.

#### Screenshot
1. Take screenshots of the visual components where each message is used within you app.
2. Name each screenshot with the corresponding message key from the `.arb` file.
3. Save the screenshots with the extension `.png`, `.jpeg`, or `.jpg`.
4. Put all such screenshots under a folder, and pass it's directory as `-s` parameter.

#### Language Options
Use the two letter language codes as parameters. 
> Warning: Some languages have not been fully tested for their availability and accuracy.

<details>
<summary>Language Code</summary>

```JSON
af: Afrikaans
am: Amharic
ar: Arabic
as: Assamese
az: Azerbaijani
be: Belarusian
bg: Bulgarian
bn: Bengali Bangla
bs: Bosnian
ca: Catalan Valencian
cs: Czech
cy: Welsh
da: Danish
de: German
el: Modern Greek
en: English
es: Spanish Castilian
et: Estonian
eu: Basque
fa: Persian
fi: Finnish
fr: French
gl: Galician
gs: Swiss German Alemannic Alsatian
gu: Gujarati
he: Hebrew
hi: Hindi
hr: Croatian
hu: Hungarian
hy: Armenian
id: Indonesian
is: Icelandic
it: Italian
ja: Japanese
ka: Georgian
kk: Kazakh
km: Khmer Central Khmer
kn: Kannada
ko: Korean
ky: Kirghiz Kyrgyz
lo: Lao
lt: Lithuanian
lv: Latvian
mk: Macedonian
ml: Malayalam
mn: Mongolian
mr: Marathi
ms: Malay
my: Burmese
nb: Norwegian Bokmål
ne: Nepali
nl: Dutch Flemish
no: Norwegian
or: Oriya
pa: Panjabi Punjabi
pl: Polish
ps: Pushto Pashto
pt: Portuguese
ro: Romanian Moldavian Moldovan
ru: Russian
si: Sinhala Sinhalese
sk: Slovak
sl: Slovenian
sq: Albanian
sr: Serbian
sv: Swedish
sw: Swahili
ta: Tamil
te: Telugu
th: Thai
tl: Tagalog
tr: Turkish
uk: Ukrainian
ur: Urdu
uz: Uzbek
vi: Vietnamese
zh: Chinese
zu: Zulu
```

</details>

### Output
The output `.arb` files will be located in the `./out` folder.

## Contact
If you have any questions, suggestions, or need further assistance, please open an issue or contact the project maintainers.