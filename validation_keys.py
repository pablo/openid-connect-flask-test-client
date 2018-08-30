from providers import google

def get_validation_key(provider: str, key_id: str):
    if provider == 'google':
        return google.get_validation_key(key_id)
    return None
