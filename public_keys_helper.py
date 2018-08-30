

def get_public_key_from_file(provider: str, kid: str):
    with open('pubkeys/{}-{}.pem'.format(provider, kid)) as f:
        ret = f.read()
        return ret