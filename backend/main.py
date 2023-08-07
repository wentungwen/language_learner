from flask import Flask, jsonify, request
from flask_cors import CORS
import requests, os
import googletrans
from google.cloud import translate_v2 as translate

app = Flask(__name__)
# app.config.from_object(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# mock data
conversations = [
    {
        "id": 1,
        "date": "2019-05-04",
        "title": "te laat",
        "messages": [
            {
                "sender": "A",
                "content": "(backend)Ik heb de treinkaarten. Twee retourtjes naar Den Haag.",
            },
            {
                "sender": "B",
                "content": "Volgens de man achter het loket, vertrekt de trein over een kwartier van spoor vijf.",
            },
            {
                "sender": "A",
                "content": "Goed zo. Ik ga even naar de wc. Weet jij waar die is?",
            },
            {
                "sender": "B",
                "content": "Ja. Daar bij de ingang. Ik blijf hier bij de koffers.",
            },
        ],
    },
    {
        "id": 2,
        "date": "2019-05-05",
        "title": "de klein tiran ",
        "messages": [
            {"sender": "A", "content": "(backend)Mamma, waar is pappa?"},
            {
                "sender": "B",
                "content": "Op kantoor, natuurlijk. Ga maar even naar buiten.",
            },
            {"sender": "A", "content": "Speel met poesje in de tuin. "},
            {
                "sender": "B",
                "content": "Maar waarom niet op straat? Met de jongens.",
            },
        ],
    },
]

## GPT
GPT_APIKEY = os.environ.get("GPT_APIKEY")
GPT_API_ENDPOINT = "https://api.openai.com/v1/completions"

## google translate
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
# TRANSLATE_API_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_text(text, source_language, target_language):
    translate_client = translate.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    result = translate_client.translate(text, source_language=source_language, target_language=target_language)
    return result["translatedText"]


def generate_conversation(lan_code, topic, sentence_num, level):
   language = googletrans.LANGUAGES[lan_code]
   prompt = f'Generate a  {language} conversation. Difficulty levels: {level}. Total {str(sentence_num)} sentences. About {topic}. In Json format, ex:[{{"sender": "A","content": "...",}},]'
   request_headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {GPT_APIKEY}"
   }
   request_data = {
      "model": "text-davinci-003",
      "prompt": prompt,
      "max_tokens": 1000,
      "temperature": 0.8
   }

   response = requests.post(GPT_API_ENDPOINT, headers=request_headers, json=request_data)

   if response.status_code == 200:
      generated_conversations = response.json()["choices"][0]["text"]
      stripped_res = generated_conversations.strip()
      return stripped_res
   else:
      print(f"Request failed with status code: {str(response.status_code), response.text}")

@app.route("/translate", methods=["GET", "POST"])
def translate_to_en():
    if request.method == "POST":
        posted_data = request.get_json()
        conversations = posted_data["conversations"]
        lan_code = posted_data["lan_code"]
        translated_conversations=conversations

        for conversation in translated_conversations:
            content = conversation.get("content")
            translated_text = translate_text(text=content, source_language=lan_code, target_language="en")
            conversation["content"] = translated_text
        print(translated_conversations)
        return jsonify({"conversations": translated_conversations})
    else:
      return "translate."


@app.route("/conversations", methods=["GET", "POST"])
def get_conversations():
    if request.method == "POST":
        posted_data = request.get_json()
        lan_code=posted_data["lan_code"]
        topic = posted_data["topic"]
        sentence_num=posted_data["sentence_num"]
        level=posted_data["level"]
        response = generate_conversation(lan_code, topic, sentence_num, level)
        return jsonify(response)
    else:
        return jsonify({"data": conversations})


if __name__ == "__main__":
    app.run(debug=True)
