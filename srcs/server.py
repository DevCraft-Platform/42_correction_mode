from flask import Flask, jsonify, request, redirect, url_for, session
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv
import os
import ssl
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session
import requests
import random
import string
import certifi

from urllib.parse import urlencode  # For handling query parameters


load_dotenv()

intra_client_id = os.getenv('INTRA_CLIENT_ID')
intra_client_secret = os.getenv('INTRA_CLIENT_SECRET')
intra_redirect_uri = os.getenv('INTRA_REDIRECT_URI')

app = Flask(__name__)
app.secret_key = os.urandom(64)  # Generate a strong, random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure secure cookies (HTTPS)

oauth = OAuth(app)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile=f"{os.getcwd()}/cert.pem", keyfile=f"{os.getcwd()}/key.pem")

request_session = Session()
intra = oauth.remote_app(
    'intra',
    consumer_key=intra_client_id,
    consumer_secret=intra_client_secret,
    request_token_params={'scope': 'public'},  # Adjust scopes as needed
    base_url='https://api.intra.42.fr/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.intra.42.fr/oauth/token',
    authorize_url='https://api.intra.42.fr/oauth/authorize'
)


# Main Route (placeholder)
@app.route('/')
def index():
    return 'OAuth Server - 42 API'


@app.route('/login')
def login():
    callback=url_for('callback', _external=True)
    state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    session['oauth_state'] = state
    response = intra.authorize(callback=callback, state=state)
    return redirect(response.location, code=response.status_code)


# Callback Route (handles redirect after authorization)
@app.route('/oauth/intra/callback')
def callback():
    state = session.get('oauth_state')
    if not state or state != request.args['state']:
        return 'Invalid state parameter', 400

    response = intra.authorized_response()
    if response is None:
        return 'Failed to fetch access token', 400

    # Access token retrieved, use it for authorized requests or store securely
    access_token = response.get('access_token')

    # Example: Make a request to a protected Intralia de 42 endpoint
    user_info_url = f'https://api.intra.42.fr/v2/me{urlencode({"access_token": access_token})}'  # URL construction with access token
    user_info = requests.get(user_info_url, verify=certifi.where())  # Verify=False to ignore SSL certificate (for testing purposes
    if user_info.status_code == 200:
        user_data = user_info.json()
        return f'Welcome, {user_data.get("login")}'  # Example, adjust based on response
    else:
        return f'Error accessing user info: {user_info.status_code}'

    return 'You are logged in!'  # Placeholder, replace with your logic

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
