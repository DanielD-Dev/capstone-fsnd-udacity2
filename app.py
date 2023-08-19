import os
from flask import Flask, request, abort, jsonify
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Movie, Actor  
from auth import AuthError, requires_auth

app = Flask(__name__)
CORS(app)
db.init_app(app)  # Initialize the database

# Auth0 Configuration
AUTH0_DOMAIN = 'ddreyman1.us.auth0.com'
API_AUDIENCE = 'casting-agency'
ALGORITHMS = ['RS256']
API_BASE_URL = 'https://ddreyman1.us.auth0.com' 


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
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


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token_auth_header()
        try:
            payload = verify_decode_jwt(token)
        except:
            abort(401)
        return f(payload, *args, **kwargs)

    return wrapper

@app.route('/headers')
@requires_auth
def headers(payload):
    print(payload)
    return 'Access Granted'



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    
    # Configure the app and database connection
    app.config.from_object('config')
    db.init_app(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        # Implement logic to retrieve actors from the database
        # Return a JSON response with the list of actors
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        # Implement logic to retrieve movies from the database
        # Return a JSON response with the list of movies
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        # Implement logic to create a new actor in the database
        # Return a JSON response with the newly created actor
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        # Implement logic to create a new movie in the database
        # Return a JSON response with the newly created movie
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        # Implement logic to update an existing actor in the database
        # Return a JSON response with the updated actor
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        # Implement logic to update an existing movie in the database
        # Return a JSON response with the updated movie
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        # Implement logic to delete an actor from the database
        # Return a JSON response indicating success
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        # Implement logic to delete a movie from the database
        # Return a JSON response indicating success
    
    # Implement the @app.errorhandler decorator for formatting error responses
    
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
