import os
import json
from flask import request, _request_ctx_stack, abort, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_ALGORITHMS = os.getenv('AUTH0_ALGORITHMS')
AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
SESSION_KEY = os.getenv('SESSION_KEY')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
    Attempts to get the header from the request
        raises an AuthError if no header is present
    Attempts to split bearer and the token
        raises an AuthError if the header is malformed
    returns the token part of the header
'''


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # print("AUTH HEAD: ", auth)
    if not auth:
        # print("No Authorization header found...")
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
    @INPUTS
        permission: string permission (i.e. 'post:actors')
        payload: decoded jwt payload

    raises an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    raises an AuthError if the requested permission string is
        not in the payload permissions array
    returns true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Permission not found.'
        }, 403)
    return True


'''
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    verifies the token using Auth0 /.well-known/jwks.json
    decodes the payload from the token
    validates the claims
    returns the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    # print("running decode jwt")
    rsa_key = {}
    if 'kid' not in unverified_header:
        # print("'\nkid' not in unverified_header\n")
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
    if not rsa_key:
        print("\nNot an rsa_key\n")
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0_ALGORITHMS,
                audience=AUTH0_API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # print("Payload: ", payload)
            return payload

        except jwt.ExpiredSignatureError:
            print("Throwing ExpiredSignatureError")
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            print("Throwing JWTClaimsError")
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. \
                    Please, check the audience and issuer.'
            }, 401)
        except Exception:
            print("Throwing Exception")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


'''
    @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:movies')

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt method to decode the jwt
    uses the check_permissions method validate claims and check the
        requested permission
    returns the decorator which passes the decoded payload to the
         decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if SESSION_KEY in session:
                token = session[SESSION_KEY]
            else:
                token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                print("Exception encountered in verify_decode_jwt")
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


'''
    @requires_auth(f) decorator method
    @INPUTS
        f: string empty ("")

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt method to decode the jwt
    returns the decorator which passes the decoded payload to the
        decorated method
'''


def requires_basic_auth(f):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if SESSION_KEY in session:
                token = session[SESSION_KEY]
            else:
                token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                abort(401)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
