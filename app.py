from flask import Flask, render_template, request
import requests
import json
import uuid

app = Flask(__name__)

subscription_key = "e66617687f6f4f6f80fdaf14d97c665b"
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = "westeurope"


@app.route('/', methods=['GET', 'POST'])
def translate():
    translation = ''
    if request.method == 'POST':
        text_to_translate = request.form['text_to_translate']
        lang_to = request.form['lang_to']

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': 'fr',
            'to': [lang_to]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': text_to_translate}]

        response = requests.post(
            constructed_url, params=params, headers=headers, json=body)
        response_json = response.json()

        translation = response_json[0]['translations'][0]['text']

    return render_template('translate.html', translation=translation)


if __name__ == "__main__":
    app.run(debug=False)
