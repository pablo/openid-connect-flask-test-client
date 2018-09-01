import base64

from Crypto.PublicKey import RSA

from providers import google

def get_validation_key(provider: str, key_id: str):
    if provider == 'google':
        vk = google.get_validation_key(key_id)
        print(vk)
        if 'n' in vk and 'e' in vk:
            n = int.from_bytes(base64.b64decode(vk['n']), 'big')
            e = int.from_bytes(base64.b64decode(vk['e']), 'big')
            k = RSA.construct((n, e,))
            print(str("\n".join(str(k.publickey().exportKey()).split('\\n'))))
            return k

    return None
