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

# Custom error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

# Custom error handler for 401 Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

# Custom error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

# Custom error handler for other internal errors
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500

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


def requires_auth(permissions):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                check_permissions(permissions, payload)
            except AuthError as auth_error:
                abort(auth_error.status_code, auth_error.error)
            return f(payload, *args, **kwargs)
        return wrapper
    return decorator

def check_permissions(permissions, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    
    if not any(permission in payload['permissions'] for permission in permissions):
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

@app.route('/headers')
@requires_auth
def headers(payload):
    print(payload)
    return 'Access Granted'



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jlvjdfmxzsjfjb:87eacc615b5b95666b397bc1b8a4698ee339abfd03b0861f6363d71c10ff5104@ec2-54-234-13-16.compute-1.amazonaws.com:5432/dc1nv8tdd0nmn5"
    db.init_app(app)  # Initialize the database

    @app.route('/actors', methods=['GET'])
    @requires_auth(['get:actors'])
    def get_actors(payload):
        try:
            actors = Actor.query.all()  # Assuming Actor is your SQLAlchemy model
            formatted_actors = [actor.format() for actor in actors]  # Format actors using a method in your model
            return jsonify({
                'success': True,
                'actors': formatted_actors
            })
        except Exception:
            abort(500)

    
    @app.route('/movies', methods=['GET'])
    @requires_auth(['get:movies'])
    def get_movies(payload):
      try:
          movies = Movie.query.all()  # Assuming Movie is your SQLAlchemy model
          formatted_movies = [movie.format() for movie in movies]  # Format movies using a method in your model
          return jsonify({
              'success': True,
              'movies': formatted_movies
          })
      except Exception:
          abort(500)
    
    @app.route('/actors', methods=['POST'])
    @requires_auth(['post:actors'])
    def create_actor(payload):
        try:
            data = request.get_json()
            new_actor = Actor(
                name=data.get('name'),
                age=data.get('age'),
                gender=data.get('gender')
            )
            db.session.add(new_actor)
            db.session.commit()
            return jsonify({
                'success': True,
                'actor': new_actor.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    @app.route('/movies', methods=['POST'])
    @requires_auth(['post:movies'])
    def create_movie(payload):
        try:
            data = request.get_json()
            new_movie = Movie(
                title=data.get('title'),
                release_date=data.get('release_date')
            )
            db.session.add(new_movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'movie': new_movie.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(['patch:actors'])
    def update_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            data = request.get_json()
            if 'name' in data:
                actor.name = data['name']
            if 'age' in data:
                actor.age = data['age']
            if 'gender' in data:
                actor.gender = data['gender']

            db.session.commit()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(['patch:movies'])
    def update_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            data = request.get_json()
            if 'title' in data:
                movie.title = data['title']
            if 'release_date' in data:
                movie.release_date = data['release_date']

            db.session.commit()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(['delete:actors'])
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            db.session.delete(actor)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Actor deleted successfully'
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(['delete:movies'])
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            db.session.delete(movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Movie deleted successfully'
            })
        except Exception:
            db.session.rollback()
            abort(500)
    
    # Custom error handler for 422 Unprocessable Entity
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    # Custom error handler for other internal errors
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
