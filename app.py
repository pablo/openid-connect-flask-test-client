import random

from flask import Flask, session, redirect, make_response

from hashlib import sha256

import oidc_config

import urllib.parse

SESSION_USER = "session.user"

app = Flask(__name__)

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

@app.route('/')
def hello_world():

    return 'Hello World!'


def redirect_authentication_request():

    state = ""
    nonce_cookie = generate_nonce()
    nonce = sha256(nonce_cookie.encode('utf-8')).hexdigest()

    redirect_url = "{}?scope={}&response_type={}&client_id={}&redirect_uri={}&state={}&nonce={}&display={}".format(
        oidc_config.Config[oidc_config.AUTHORIZATION_ENDPOINT], # URL for redirection,
        "openid", #scope
        "code", # response_type
        urllib.parse.quote(oidc_config.Config[oidc_config.CLIENT_ID]), # client_id
        urllib.parse.quote(oidc_config.Config[oidc_config.REDIRECT_URI]), # redirect_uri
        urllib.parse.quote(state), # state
        urllib.parse.quote(nonce), # nonce
        urllib.parse.quote("page")
    )

    response = make_response(redirect(redirect_url, 302))
    response.set_cookie('nonce', nonce_cookie, httponly=True)

    return response

@app.route('/secured')
def secured_resource():
    if SESSION_USER in session:
        return ''
    else:
        # redirect to login
        return redirect_authentication_request()


if __name__ == '__main__':
    app.run(debug=True)
