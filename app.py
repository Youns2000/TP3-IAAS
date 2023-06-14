from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
import requests
import json
import uuid
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__, static_folder='static/build', static_url_path='/')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.secret_key = 'nOsv22uBT0pA23LYNj3iIaUUMZ4Wv9ga'
oauth = OAuth(app)
CORS(app)

microsoft = oauth.register(
    'microsoft',
    # Azure AD client id
    client_id='e6cf219a-980d-40c9-8e8c-77ffaf8686db',
    # Azure AD client secret
    client_secret='LS48Q~mvcsrAgnJvQ9s7CRNVA1gGjftFc~O4ydsP',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    api_base_url='https://graph.microsoft.com/v1.0/',
    client_kwargs={'scope': 'User.Read'},
)

subscription_key = "e66617687f6f4f6f80fdaf14d97c665b"
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = "westeurope"


@app.route('/')
def index():
    email = dict(session).get('email', None)
    if email:
        # return render_template('translate.html')
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True, _scheme='https')
    return microsoft.authorize_redirect(redirect_uri)


@app.route('/login/authorized')
def authorize():
    token = microsoft.authorize_access_token()
    resp = microsoft.get('me')
    session['email'] = resp.json().get('userPrincipalName')
    return redirect('/')


@app.route('/translate', methods=['POST'])
def translate():
    translation = ''
    if 'email' in session:  # Check if the user is logged in
        # text_to_translate = request.form['text_to_translate']
        # lang_to = request.form['lang_to']
        data = request.get_json()
        text_to_translate = data['text_to_translate']
        lang_to = data['lang_to']

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

        # return render_template('translate.html', translation=translation)
        return jsonify({'translation': translation})
    else:  # The user is not logged in, redirect to login page
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
