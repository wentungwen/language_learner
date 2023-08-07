import os
import requests
from google.cloud import translate_v2 as translate

## google translate
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
api_endpoint = "https://translation.googleapis.com/language/translate/v2"

print(GOOGLE_APPLICATION_CREDENTIALS)

def translate_text(text, source_language, target_language):
    translate_client = translate.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    result = translate_client.translate(text, source_language=source_language, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    text_to_translate = "Bonjour, tout le monde!"  # French text
    source_language = "fr"  # Source language: French
    target_language = "nl"  # Target language: Dutch

    translated_text = translate_text(text_to_translate, source_language, target_language)
    print("Original Text (French): ", text_to_translate)
    print("Translated Text (Dutch): ", translated_text)


## gpt testing
# api_endpoint = "https://api.openai.com/v1/completions"
# api_key = os.environ.get("GPT_APIKEY")

# request_headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer " + api_key
# }
# prompt = "A man walks into a bar, translate to dutch"

# request_data = {
#     "model": "text-davinci-003",
#     "prompt": prompt,
#     "max_tokens": 1000,
#     "temperature": 0.8
# }

# response = requests.post(api_endpoint, headers=request_headers, json=request_data)

# if response.status_code == 200:
#     response_text = response.json()["choices"][0]["text"]
#     print(response_text)
# else:
#     print(f"Request failed with status code: {str(response.status_code), response.text}")
