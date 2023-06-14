from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from pdfminer.high_level import extract_text
from docx import Document
from io import StringIO
import requests
import json
import uuid
# import magic
import mimetypes
import config
import os


app = Flask(__name__, static_folder='static/build', static_url_path='/')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.secret_key = config.SECRET_KEY
oauth = OAuth(app)
CORS(app)

microsoft = oauth.register(
    'microsoft',
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    api_base_url='https://graph.microsoft.com/v1.0/',
    client_kwargs={'scope': 'User.Read'},
)

subscription_key = config.SUBSCRIPTION_KEY
endpoint = config.ENDPOINT
location = config.LOCATION


@app.route('/')
def index():
    email = dict(session).get('email', None)
    if email:
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True, _scheme=(
        "https" if not config.LOCAL else "http"))
    return microsoft.authorize_redirect(redirect_uri)


@app.route('/login/authorized')
def authorize():
    token = microsoft.authorize_access_token()
    resp = microsoft.get('me')
    session['email'] = resp.json().get('userPrincipalName')
    return redirect('/')


@app.route('/email', methods=['GET'])
def get_email():
    email = dict(session).get('email', None)
    if email:
        return jsonify({'email': email})
    else:
        return redirect(url_for('login'))


@app.route('/translate', methods=['POST'])
def translate():
    translation = ''
    if 'email' in session:
        file = request.files.get('file')
        lang_from = request.form['lang_from']
        lang_to = request.form['lang_to']
        if file:
            mime, _ = mimetypes.guess_type(file.filename)
            file.seek(0)
            if mime == 'application/pdf':
                temp_filename = "temp_file.pdf"
                file.save(temp_filename)
                text_to_translate = extract_text(temp_filename)
                os.remove(temp_filename)
                # text_to_translate = extract_text(file)
            elif mime == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                doc = Document(file)
                text_to_translate = ' '.join([p.text for p in doc.paragraphs])
            elif mime == 'text/plain':
                text_to_translate = file.read().decode()
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
        else:
            text_to_translate = request.form['text_to_translate']

        # print(text_to_translate, lang_from, lang_to)

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': [lang_from],
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

        return jsonify({'translation': translation})
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=False)
