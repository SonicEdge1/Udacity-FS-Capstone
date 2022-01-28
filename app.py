import os
from flask import Flask, request, abort, jsonify, session, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from datetime import date
import codes as Codes
from database.models import setup_db, Actor, Movie, actor_bookings, AuthError
from auth.auth import AuthError, requires_auth, requires_basic_auth

from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from dotenv import load_dotenv, find_dotenv
from functools import wraps
from os import environ as env



AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_API_BASE_URL = os.getenv('AUTH0_API_BASE_URL')
# AUTH0_CALLBACK_URL = os.getenv('AUTH0_REMOTE_CALLBACK_URL')  # comment this line to run loacally
AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')       # uncomment this line for running locally
AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
SESSION_TYPE = 'sqlalchemy'
SESSION_KEY = os.getenv('SESSION_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
database_filename = "database.db"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='templates')
    # ???? is this the correct place for this?
    setup_db(app, database_filename)
    app.secret_key = SECRET_KEY

    CORS(app)

    oauth = OAuth(app)
    AUTH0_API_BASE_URL = os.getenv('AUTH0_API_BASE_URL')

    AUTH0_API_BASE_URL = 'https://joes-casting-agency.us.auth0.com'

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_API_BASE_URL,
        access_token_url=AUTH0_API_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_API_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email'
        }
    )

    ###############################
    # Log-in / Log-out Handling ###
    ###############################
    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(
            redirect_uri=AUTH0_CALLBACK_URL,
            audience=AUTH0_API_AUDIENCE)

    # Here we're using the /callback route.
    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        token = auth0.authorize_access_token()
        # stores bearer token in session
        session[SESSION_KEY] = token[SESSION_KEY]
        print("Session Token::   ")
        print(session[SESSION_KEY])
        print(" ...Token End.")
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')

    @app.route('/dashboard')
    @requires_basic_auth("")
    def dashboard(payload):
        return render_template(
            'dashboard.html',
            userinfo=session['profile'],
            userinfo_pretty=json.dumps(
                session['jwt_payload'],
                indent=4))

    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {
            'returnTo': url_for(
                'home',
                _external=True),
            'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url +
                        '/v2/logout?' + urlencode(params))

    # ROUTES ##################

    @app.route('/movie-list')
    @requires_auth('get:actors-and-movies')
    def movie_list(payload):
        return render_template('movie-list.html')

    @app.route('/actor-list')
    @requires_auth('get:actors-and-movies')
    def actor_list(payload):
        return render_template('actor-list.html')

    @app.route('/')
    def test_alive():
        try:
            return jsonify({
                'success': True,
                'message': "Hello World",
            }), Codes.OK
        except Exception as e:
            # print("Exception: ", e)
            abort(Codes.UNPROCESSABLE_ENTITY)

    ##################################################
    # ACTOR INTERFACE ################################
    ##################################################

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors-and-movies')
    def get_actors(payload):
        try:
            all_actors = Actor.query.all()
            actors = [actor.format() for actor in all_actors]
            return jsonify({
                'success': True,
                'actors': actors,
                'total_actors': len(Actor.query.all()),
            }), Codes.OK
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors-and-movies')
    def get_actor(payload, actor_id):
        queried_actor = Actor.query.get(actor_id)
        if queried_actor is None:
            print("actor_id: ", actor_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            movies = queried_actor.movies.all()
            movie_list = []
            for movie in movies:
                movie_list.append(movie.format())
            return jsonify({
                'success': True,
                'actor': queried_actor.format(),
                'cast_in': movie_list
            })
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(payload):
        try:
            body = request.get_json()
            new_actor_name = body.get('name')
            new_actor_age = body.get('age')
            new_actor_gender = body.get('gender')
            if (new_actor_name is None or new_actor_age is None
                    or new_actor_gender is None):
                raise TypeError("Actor is Missing a Required Value")
            new_actor = Actor(
                name=new_actor_name,
                age=new_actor_age,
                gender=new_actor_gender
            )
            new_actor.insert()
            return jsonify({
                'success': True,
                'added_actor': new_actor.format(),
                'total_actors': len(Actor.query.all()),
            })
        except TypeError as e:
            abort(Codes.BAD_REQUEST)
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors-and-movies')
    def modify_actor(payload, actor_id):
        queried_actor = Actor.query.get(actor_id)
        if queried_actor is None:
            print("actor_id: ", actor_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            body = request.get_json()
            edited_actor_name = body.get('name')
            if edited_actor_name is not None:
                queried_actor.name = edited_actor_name
            edited_actor_age = body.get('age')
            if edited_actor_age is not None:
                queried_actor.age = edited_actor_age
            edited_actor_gender = body.get('gender')
            if edited_actor_gender is not None:
                queried_actor.gender = edited_actor_gender
            queried_actor.update()
            return jsonify({
                'success': True,
                'actor': queried_actor.format(),
            })
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            print("actor_id: ", actor_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            name = actor.name
            actor.delete()
            return jsonify({
                "success": True,
                "deleted_actor_id": actor_id,
                "deleted_actor_name": name,
            })
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    ###############################################
    # MOVIE INTERFACE #############################
    ###############################################

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:actors-and-movies')
    def get_movies(payload):
        try:
            all_movies = Movie.query.all()
            movies = [movie.format() for movie in all_movies]

            return jsonify({
                'success': True,
                'movies': movies,
                'total_movies': len(Movie.query.all()),
            }), Codes.OK
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:actors-and-movies')
    def get_movie(payload, movie_id):
        queried_movie = Movie.query.get(movie_id)
        if queried_movie is None:
            print("movie_id: ", movie_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            actors = queried_movie.actors.all()
            actor_list = []
            for actor in actors:
                actor_list.append(actor.format())
            return jsonify({
                'success': True,
                'movie': queried_movie.format(),
                'movie_cast': actor_list
            })
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(payload):
        try:
            body = request.get_json()
            new_movie_title = body.get('title')
            new_movie_year = body.get('release_year')
            new_movie_month = body.get('release_month')
            new_movie_day = body.get('release_day')
            new_movie_actor_ids = body.get('actors')
            if (new_movie_title is None or new_movie_year is None
                    or new_movie_month is None or new_movie_day is None):
                raise TypeError("Movie is Missing a Required Value")
            if int(new_movie_year) < 1888:  # date of first motion picture
                raise ValueError("invalid year")
            new_actor_object_list = []
            if new_movie_actor_ids is not None:
                for actor_id in new_movie_actor_ids:
                    actor_object = Actor.query.get(actor_id)
                    if actor_object is None:
                        raise KeyError("No Existing Actor for ID: ", actor_id)
                    else:
                        new_actor_object_list.append(actor_object)
            new_movie = Movie(
                title=new_movie_title,
                releaseDate=date(
                    int(new_movie_year),
                    int(new_movie_month),
                    int(new_movie_day)),
                actors=new_actor_object_list)
            new_movie.insert()
            formatted_actors = []
            for actor in new_actor_object_list:
                formatted_actors.append(actor.format())

            return jsonify({
                'success': True,
                'added_movie': new_movie.format(),
                'total_movies': len(Movie.query.all()),
                'movie_cast': formatted_actors,
            })
        except TypeError as e:
            abort(Codes.BAD_REQUEST)
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:actors-and-movies')
    def modify_movie(payload, movie_id):
        queried_movie = Movie.query.get(movie_id)
        if queried_movie is None:
            print("movie_id: ", movie_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            body = request.get_json()
            edited_movie_title = body.get('title')
            if edited_movie_title is not None:
                queried_movie.title = edited_movie_title
            edited_movie_year = body.get('release_year')
            edited_movie_month = body.get('release_month')
            edited_movie_day = body.get('release_day')
            # if date is edited properly
            if (edited_movie_year is not None
                    and edited_movie_month is not None
                    and edited_movie_day is not None):
                queried_movie.releaseDate = date(
                    int(edited_movie_year),
                    int(edited_movie_month),
                    int(edited_movie_day))
            # if date is completely omitted
            elif (edited_movie_year is None
                    and edited_movie_month is None
                    and edited_movie_day is None):
                pass
            # if only partial date data exists
            else:
                raise ValueError("Missing input for a date value")
            edited_movie_actor_ids = body.get('actors')
            edited_actor_object_list = []
            if edited_movie_actor_ids is not None:
                for actor_id in edited_movie_actor_ids:
                    actor_object = Actor.query.get(actor_id)
                    if actor_object is None:
                        raise ValueError(
                            "No Existing Actor for ID: ", actor_id)
                    else:
                        edited_actor_object_list.append(actor_object)
            queried_movie.actors = edited_actor_object_list
            queried_movie.update()
            formatted_actors = []
            for actor in edited_actor_object_list:
                formatted_actors.append(actor.format())
            return jsonify({
                'success': True,
                'movie': queried_movie.format(),
                'movie_cast': formatted_actors,
            })
        except ValueError as ve:
            print(ve)
            abort(Codes.BAD_REQUEST)
        except Exception as e:
            abort(Codes.UNPROCESSABLE_ENTITY)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            print("movie_id: ", movie_id)
            abort(Codes.RESOURCE_NOT_FOUND)
        try:
            title = movie.title
            movie.delete()
            return jsonify({
                'success': True,
                'deleted_movie_id': movie_id,
                'deleted_movie_title': title,
            })
        except Exception as e:
            # print("Exception: ", e)
            abort(Codes.UNPROCESSABLE_ENTITY)

    #######################################
    # Error Handling ######################
    #######################################

    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": Codes.BAD_REQUEST,
            "message": Codes.BAD_REQUEST_MSG
        }), Codes.BAD_REQUEST

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": Codes.RESOURCE_NOT_FOUND,
            "message": Codes.RESOURCE_NOT_FOUND_MSG
        }), Codes.RESOURCE_NOT_FOUND

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": Codes.UNPROCESSABLE_ENTITY,
            "message": Codes.UNPROCESSABLE_ENTITY_MSG
        }), Codes.UNPROCESSABLE_ENTITY

    @app.errorhandler(AuthError)
    def auth_error(error):
        # 401
        # print("error: ", error.status_code)
        if error.status_code == Codes.UNAUTHORIZED:
            return jsonify({
                "success": False,
                "error": Codes.UNAUTHORIZED,
                "message": Codes.UNAUTHORIZED_MSG
            }), Codes.UNAUTHORIZED
        # 403
        elif error.status_code == Codes.FORBIDDEN:
            return jsonify({
                "success": False,
                "error": Codes.FORBIDDEN,
                "message": Codes.FORBIDDEN_MSG
            }), Codes.FORBIDDEN
        # 400
        elif error.status_code == Codes.BAD_REQUEST:
            return jsonify({
                "success": False,
                "error": Codes.BAD_REQUEST,
                "message": Codes.BAD_REQUEST_MSG
            }), Codes.BAD_REQUEST
        else:
            return jsonify({
                "success": False,
                "error": Codes.NTERNAL_SERVER_ERROR,
                "message": Codes.INTERNAL_SERVER_ERROR_MSG
            }), Codes.INTERNAL_SERVER_ERROR

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
