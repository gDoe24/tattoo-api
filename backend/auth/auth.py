import os
import json
from flask import Flask, request, jsonify, _request_ctx_stack, abort
from flask_cors import cross_origin
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = [os.environ.get('ALGORITHMS')]
API_AUDIENCE = os.environ.get('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
Get the authorization token from the request header
'''


def get_token_auth_header():

    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
                        'code': 'authorization_header_missing',
                        'description': 'Authoriation header not found'
                        }, 401)

    header_parts = auth.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
                        'code': 'invalid_header',
                        'description': "header parts != 2"
                        }, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
                        'code': 'invalid_header',
                        'description': 'header must start with Bearer'
                        }, 401)

    return header_parts[1]


'''
Check the authorization token for the required permissions
to access the requested endpoint
'''


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        abort(401)

    if permission not in payload['permissions']:
        abort(401)

    return True


'''
Token decoder to validate the token uses Auth0 and
return the decoded payload
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
Requires Authorization decorator method used to validate requests
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
