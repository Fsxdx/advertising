from base64 import b64decode


def is_auth_request_valid(api_request):
    auth_header = api_request.headers.get('Authorization', '')
    if not auth_header or len(auth_header) <= len('basic'):
        return False
    return True


def decode_basic_authorization(api_request):
    auth_header = api_request.headers.get("Authorization")
    token = auth_header.split(' ')[-1]
    login_and_password = b64decode(token.encode('ascii')).decode('ascii').split(':')
    if len(login_and_password) != 2:
        raise ValueError('Invalid Basic Authorization header')
    login, password = login_and_password
    return login, password
