# flask

APP_SECRET_KEY = b'this is it'

# OpenID

OIDC_PROVIDER = 'google'

# as an example, we use Google's
AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_EXCHANGE_ENDPOINT = 'https://www.googleapis.com/oauth2/v4/token'

REDIRECT_URI = 'http://lvh.me:5000/auth_result'

OIDC_CLIENT_ID = 'insert_your_client_id_here'
OIDC_CLIENT_SECRET = 'insert_your_client_secret_here'

try:
    from local_config import *
except:
    pass