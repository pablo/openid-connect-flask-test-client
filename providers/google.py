import requests
from http import HTTPStatus

DISCOVERY_ENDPOINT = 'https://accounts.google.com/.well-known/openid-configuration'

_dinfo = None


def get_discovery_info():
    global _dinfo
    if not _dinfo:
        dr = requests.get(DISCOVERY_ENDPOINT)
        if dr.status_code == HTTPStatus.OK:
            _dinfo = dr.json()
    return _dinfo


_keys = {}


def do_load_google_keys(url: str):
    dr = requests.get(url)
    if dr.status_code == HTTPStatus.OK:
        keys_info = dr.json()
        if 'keys' in keys_info:
            for key in keys_info['keys']:
                _keys[key['kid']] = key


def get_validation_key(key_id: str):
    global _keys
    if key_id in _keys:
        return _keys[key_id]

    dinfo = get_discovery_info()

    keyinfo_url = dinfo['jwks_uri']

    do_load_google_keys(keyinfo_url)

    return _keys[key_id] if key_id in _keys else None
