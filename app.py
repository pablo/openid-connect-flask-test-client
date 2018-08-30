import os

import random

import jwt
import requests
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

import config

from flask import Flask, request, session, redirect, make_response, render_template
from http import HTTPStatus

from hashlib import sha256

import urllib.parse

import validation_keys

SESSION_USER = "session.user"

app = Flask(__name__, static_url_path='/static')
app.secret_key = config.APP_SECRET_KEY

jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

@app.route('/')
def index():
    return render_template('index.html')


def redirect_authentication_request():

    # state
    state = sha256(os.urandom(1024)).hexdigest()
    session['state'] = state

    # nonce
    nonce_cookie = generate_nonce()
    nonce = sha256(nonce_cookie.encode('utf-8')).hexdigest()

    redirect_url = "{}?scope={}&response_type={}&client_id={}&redirect_uri={}&state={}&nonce={}&display={}".format(
        config.AUTHORIZATION_ENDPOINT, # URL for redirection,
        urllib.parse.quote("openid email"), #scope
        "code", # response_type
        urllib.parse.quote(config.OIDC_CLIENT_ID), # client_id
        urllib.parse.quote(config.REDIRECT_URI), # redirect_uri
        urllib.parse.quote(state), # state
        urllib.parse.quote(nonce), # nonce
        urllib.parse.quote("page")
    )

    response = make_response(redirect(redirect_url, HTTPStatus.FOUND))
    response.set_cookie('nonce', nonce_cookie, httponly=True)

    return response

@app.route('/secured')
def secured_resource():
    if SESSION_USER in session:
        return ''
    else:
        # redirect to login
        return redirect_authentication_request()

def return_error(err_code: str, state: str, http_status: int, err_description: str = None):
    return render_template(
        'auth_error.html',
        error = err_code,
        error_description = err_description,
        state = state
    ), http_status



@app.route('/auth_result')
def auth_result():
    state = request.args.get('state'),
    if 'error' in request.args:
        return return_error(
            request.args.get('error'),
            state,
            HTTPStatus.UNAUTHORIZED,
            "Server returned: {}".format(request.args.get('error_description'))
        )
    else:
        #session_state = session['state']

        #if session_state != state:
        if False:
            return return_error(
                'invalid_state',
                state,
                HTTPStatus.UNAUTHORIZED,
                "State in Session is: {}".format(session_state)
            )
        else:
            # exchange CODE with ACCESS TOKEN
            code = request.args.get('code')
            if not code:
                return return_error('missing_parameter', state, HTTPStatus.UNAUTHORIZED, 'Missing [code] parameter')

            params = {
                "code": code,
                "client_id": config.OIDC_CLIENT_ID,
                "client_secret": config.OIDC_CLIENT_SECRET,
                "redirect_uri": config.REDIRECT_URI,
                "grant_type": "authorization_code"
            }

            try:
                r = requests.post(config.TOKEN_EXCHANGE_ENDPOINT, data = params)
                if r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
                    token_data = r.json() # access_token, id_token, expires_in, token_type, refresh_token
                    print(token_data)
                    jwt_id_token = token_data['id_token']
                    h = jwt.get_unverified_header(jwt_id_token)
                    print(h)
                    public_key = validation_keys.get_validation_key(config.OIDC_PROVIDER, h['kid'])
                    jd = jwt.decode(token_data['id_token'], public_key, algorithms=[h['alg']], audience=config.OIDC_CLIENT_ID)
                    print(jd)
                    return render_template('auth_ok.html', jwtok = jd)
                else:
                    error_data = r.json()
                    print(error_data)
                    if 'error' in error_data:
                        err_description = error_data['error']
                    else:
                        err_description = 'Missing error information'
                    return return_error('invalid_status_from_token_endpoint', state, r.status_code, 'Status: {} Error: {}'.format(r.status_code, err_description))

            except Exception as e:
                print(e)
                return return_error('unexpected_exception', state, HTTPStatus.INTERNAL_SERVER_ERROR, 'Error: {}'.format(str(e)))


if __name__ == '__main__':
    app.run(debug=True)
