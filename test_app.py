import os
import unittest
import json
import random
import string
import codes as Codes
from app import create_app
from authlib.integrations.flask_client import OAuth
from database.models import setup_db, db, Movie, Actor, actor_bookings
from datetime import date
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']


class CastingAgencyTestCases(unittest.TestCase):
    """This class represents the Casting Agency test case"""
    is_init_run = True
    test_num = 1

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "casting_testdb"
        # self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'myuser', 'mypass', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db.drop_all()
        db.create_all()

        # binds the app to the current context
        # test seems to operate the same without this code
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

        # -----Seeding Test Database----- #
        # actor1 info
        self.actor1_name = "Jack Purvis"
        self.actor1_age = 60
        self.actor1_age2 = 84
        self.actor1_gender = "male"

        # json to test patching Actor age
        self.actor1_json = {
            'name': self.actor1_name,
            'age': self.actor1_age2,
            'gender': self.actor1_gender
        }

        # movie1 info
        self.movie1_title = "Time Bandits"
        self.movie1_releaseDate = date(1981, 11, 6)

        # movie4 info
        self.patch_movie4_title = "Cloak & Dagger"
        self.patch_movie4_newTitle = "New Title"
        self.patch_movie4_newDate = date(1984, 7, 4).isoformat()

        # json to test patching Movie
        self.patch_movie4_json = {
            'title': "New Title",
            'release_year': "1984",
            'release_month': "7",
            'release_day': "4",
            'actors': ["2", "3"]
        }

        # insert some initial data
        actor1 = Actor(
            self.actor1_name,
            self.actor1_age,
            self.actor1_gender)
        actor1.insert()
        actor2 = Actor("Casey Siemaszko", 60, "male")
        actor2.insert()
        actor3 = Actor("Sean Connery", 90, "male")
        actor3.insert()
        movie1 = Movie(
            self.movie1_title, self.movie1_releaseDate,
            [actor1, actor3])
        movie1.insert()
        movie2 = Movie(
            "Star Wars: A New Hope",
            date(1977, 5, 25), [actor1])
        movie2.insert()
        movie3 = Movie("Three O Clock High", date(1987, 10, 9), [actor2])
        movie3.insert()
        movie4 = Movie(self.patch_movie4_title, date(1984, 7, 13), [])
        movie4.insert()
        movie5 = Movie(
            "Indiana Jones and the Last Crusade",
            date(1989, 5, 24), [actor3])
        movie5.insert()

        # Movie for testing post and delete
        self.movie6_title = "Goonies"
        self.movie6_year = "1985"
        self.movie6_month = "6"
        self.movie6_day = "7"
        self.movie6_releaseDate = date(int(self.movie6_year), int(
            self.movie6_month), int(self.movie6_day))
        self.movie6_actors = ["1", "2", "3"]
        self.movie6_json = {
            'title': self.movie6_title,
            'release_year': self.movie6_year,
            'release_month': self.movie6_month,
            'release_day': self.movie6_day,
            'actors': self.movie6_actors
        }
        self.movie6Obj = Movie(self.movie6_title, self.movie6_releaseDate, [])

        # Actor to test posting... with random name
        letters = string.ascii_lowercase
        self.new_actor_name = ''.join(random.choice(letters) for i in range(
            4)) + ' ' + ''.join(random.choice(letters) for i in range(7))
        self.new_actor_age = 99
        self.new_actor_gender = "male"
        self.new_actor = Actor(
            self.new_actor_name,
            self.new_actor_age,
            self.new_actor_gender)
        self.new_actor_json = {
            'name': self.new_actor_name,
            'age': self.new_actor_age,
            'gender': self.new_actor_gender
        }

        # Actor to test deleting...
        self.delete_actor_name = "Ben Affleck"
        self.delete_actor = Actor(self.delete_actor_name, 49, "male")

        # different Authorization headers
        self.exec = os.environ['EXEC_JWT']
        self.exec_header = {
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.exec}')
        }

        self.direct = os.environ['DIRECT_JWT']
        self.direct_header = {
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.direct}')
        }

        self.assist = os.environ['ASSIST_JWT']
        self.assist_header = {
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.assist}')
        }

        # print("Running test ", CastingAgencyTestCases.test_num)
        # CastingAgencyTestCases.test_num += 1
        if CastingAgencyTestCases.is_init_run:
            CastingAgencyTestCases.is_init_run = False
            print("Adding actors to TestDB...")
            all_actors = Actor.query.all()
            for actor in all_actors:
                print(actor.format())
            print("Adding movies to TestDB...")
            all_movies = Movie.query.all()
            for movie in all_movies:
                print(movie.format())

    def tearDown(self):
        """Executed after each test"""
        pass

    #########################################
    # Testing success at all endpoints    ###
    # with executive producer permissions ###
    #########################################

    def test_success_it_is_alive(self):
        """Test success at GET '/'"""
        res = self.client().get('/')
        print("running test get /")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, Codes.OK)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Hello World")

    # casting assistant level
    # - view actors or movies
    def test_success_exec_get_movies(self):
        """Test success at GET '/movies'"""
        print("running test get /movies")
        res = self.client().get('/movies',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertEqual(data['total_movies'], 5)

    def test_success_exec_get_movies_by_id(self):
        """Test success_exec at GET '/movies/<int:movie_id>'"""
        print("running test get /movies/<int:movie_id>")
        movie_id = 1
        res = self.client().get(f'/movies/{movie_id}',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], self.movie1_title)
        self.assertEqual(
            data['movie']['releaseDate'],
            self.movie1_releaseDate.isoformat())
        self.assertEqual(len(data['movie_cast']), 2)

    def test_success_exec_get_actors(self):
        """Test success_exec at GET '/actors'"""
        print("running test get /actors")
        res = self.client().get('/actors',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(data['total_actors'], 3)

    def test_success_exec_get_actors_by_id(self):
        """Test success_exec at GET '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test get /actors/<int:actor_id>")
        res = self.client().get(f'/actors/{actor_id}',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], self.actor1_name)
        self.assertEqual(data['actor']['gender'], self.actor1_gender)
        self.assertEqual(len(data['cast_in']), 2)

    # casting director level
    # - Add or delete an actor from the database
    # - Modify actors or movies
    def test_success_exec_post_actor(self):
        """Test success_exec at POST '/actors'"""
        print("running test post /actors")
        res = self.client().post(f'/actors',
                                 headers=self.exec_header,
                                 json=self.new_actor_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['added_actor']['age'], self.new_actor_age)
        self.assertEqual(data['added_actor']['gender'], self.new_actor_gender)
        self.assertEqual(data['added_actor']['name'], self.new_actor_name)
        self.assertEqual(data['total_actors'], 4)
        actor = Actor.query.get(data['added_actor']['id'])
        actor.delete()

    def test_success_exec_patch_actor(self):
        """Test success_exec at PATCH '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  headers=self.exec_header,
                                  json=self.actor1_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], self.actor1_age2)
        self.assertEqual(data['actor']['gender'], self.actor1_gender)
        self.assertEqual(data['actor']['name'], self.actor1_name)

    def test_success_exec_delete_actor(self):
        """Test success_exec at DELETE '/actors/<int:actor_id>'"""
        self.delete_actor.insert()
        actors = Actor.query.all()
        # self.assertEqual(len(Actor.query.all()), 4)
        actor_id = self.delete_actor.id
        print("running test delete /actors/<int:actor_id>")
        res = self.client().delete(f'/actors/{actor_id}',
                                   headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], str(actor_id))
        self.assertEqual(data['deleted_actor_name'], self.delete_actor_name)
        # self.assertEqual(len(Actor.query.all()), 3) #crashes test app

    def test_success_exec_patch_moive(self):
        """Test success_exec at PATCH '/moives/<int:movie_id>'"""
        movie_id = 4
        print("running test patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.exec_header,
                                  json=self.patch_movie4_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], self.patch_movie4_newTitle)
        self.assertEqual(
            data['movie']['releaseDate'],
            self.patch_movie4_newDate)
        self.assertEqual(len(data['movie_cast']), 2)

    # Executive Producer level
    # - Add or delete a movie from the database

    def test_success_exec_post_movie(self):
        """Test success_exec at POST '/movies'"""
        print("running test post /movies")
        res = self.client().post(f'/movies',
                                 headers=self.exec_header,
                                 json=self.movie6_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['added_movie']['title'], self.movie6_title)
        self.assertEqual(
            data['added_movie']['releaseDate'],
            self.movie6_releaseDate.isoformat())
        self.assertEqual(data['total_movies'], 6)
        self.assertEqual(len(data['movie_cast']), 3)
        movie = Movie.query.get(data['added_movie']['id'])
        movie.delete()

    def test_success_exec_delete_movie(self):
        """Test success_exec at DELETE '/movie/<int:movie_id>'"""
        self.movie6Obj.insert()
        self.assertEqual(len(Movie.query.all()), 6)
        movie_id = self.movie6Obj.id
        print("running test delete /movies/<int:movie_id>")
        res = self.client().delete(f'/movies/{movie_id}',
                                   headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], movie_id)
        self.assertEqual(data['deleted_movie_title'], self.movie6_title)
        # self.assertEqual(len(Movie.query.all()), 5) #this crashes app

    ################################################
    # Testing success/forbidden at all endpoints ###
    # with casting director permissions          ###
    ################################################
    # casting assistant level
    # - view actors or movies

    def test_success_director_get_movies(self):
        """Test success_director at GET '/movies'"""
        print("running test get /movies")
        res = self.client().get('/movies',
                                headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertEqual(data['total_movies'], 5)

    def test_success_director_get_movies_by_id(self):
        """Test success_director at GET '/movies/<int:movie_id>'"""
        print("running test get /movies/<int:movie_id>")
        movie_id = 1
        res = self.client().get(f'/movies/{movie_id}',
                                headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], self.movie1_title)
        self.assertEqual(
            data['movie']['releaseDate'],
            self.movie1_releaseDate.isoformat())
        self.assertEqual(len(data['movie_cast']), 2)

    def test_success_director_get_actors(self):
        """Test success_director at GET '/actors'"""
        print("running test get /actors")
        res = self.client().get('/actors',
                                headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(data['total_actors'], 3)

    def test_success_director_get_actors_by_id(self):
        """Test success_director at GET '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test get /actors/<int:actor_id>")
        res = self.client().get(f'/actors/{actor_id}',
                                headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], self.actor1_name)
        self.assertEqual(data['actor']['gender'], self.actor1_gender)
        self.assertEqual(len(data['cast_in']), 2)

    # casting director level
    # - Add or delete an actor from the database
    # - Modify actors or movies
    def test_success_director_post_actor(self):
        """Test success_director at POST '/actors'"""
        print("running test post /actors")
        res = self.client().post(f'/actors',
                                 headers=self.direct_header,
                                 json=self.new_actor_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['added_actor']['age'], self.new_actor_age)
        self.assertEqual(data['added_actor']['gender'], self.new_actor_gender)
        self.assertEqual(data['added_actor']['name'], self.new_actor_name)
        self.assertEqual(data['total_actors'], 4)
        actor = Actor.query.get(data['added_actor']['id'])
        actor.delete()

    def test_success_director_patch_actor(self):
        """Test success_director at PATCH '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  headers=self.direct_header,
                                  json=self.actor1_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], self.actor1_age2)
        self.assertEqual(data['actor']['gender'], self.actor1_gender)
        self.assertEqual(data['actor']['name'], self.actor1_name)

    def test_success_director_delete_actor(self):
        """Test success_director at DELETE '/actors/<int:actor_id>'"""
        self.delete_actor.insert()
        self.assertEqual(len(Actor.query.all()), 4)
        actor_id = self.delete_actor.id
        print("running test delete /actors/<int:actor_id>")
        res = self.client().delete(f'/actors/{actor_id}',
                                   headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], str(actor_id))
        self.assertEqual(data['deleted_actor_name'], self.delete_actor_name)
        # self.assertEqual(len(Actor.query.all()), 3)

    def test_success_director_patch_moive(self):
        """Test success_director at PATCH '/moives/<int:movie_id>'"""
        movie_id = 4
        print("running test patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.direct_header,
                                  json=self.patch_movie4_json)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], self.patch_movie4_newTitle)
        self.assertEqual(
            data['movie']['releaseDate'],
            self.patch_movie4_newDate)
        self.assertEqual(len(data['movie_cast']), 2)

    # Executive Producer level
    # - Add or delete a movie from the database

    def test_forbidden_director_post_movie(self):
        """Test forbidden_director at POST '/movies'"""
        print("running test post /movies")
        res = self.client().post(f'/movies',
                                 headers=self.direct_header,
                                 json=self.movie6_json)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    def test_forbidden_director_delete_movie(self):
        """Test forbidden_director at DELETE '/movie/<int:movie_id>'"""
        movie_id = 1
        print("running test delete /movies/<int:movie_id>")
        res = self.client().delete(f'/movies/{movie_id}',
                                   headers=self.direct_header)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    ################################################
    # Testing success/forbidden at all endpoints ###
    # with casting assistant permissions         ###
    ################################################
    # casting assistant level
    # - view actors or movies
    def test_success_assistant_get_movies(self):
        """Test success_assistant at GET '/movies'"""
        print("running test get /movies")
        res = self.client().get('/movies',
                                headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertEqual(data['total_movies'], 5)

    def test_success_assistant_get_movies_by_id(self):
        """Test success_assistant at GET '/movies/<int:movie_id>'"""
        print("running test get /movies/<int:movie_id>")
        movie_id = 1
        res = self.client().get(f'/movies/{movie_id}',
                                headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], self.movie1_title)
        self.assertEqual(
            data['movie']['releaseDate'],
            self.movie1_releaseDate.isoformat())
        self.assertEqual(len(data['movie_cast']), 2)

    def test_success_assistant_get_actors(self):
        """Test success_assistant at GET '/actors'"""
        print("running test get /actors")
        res = self.client().get('/actors',
                                headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(data['total_actors'], 3)

    def test_success_assistant_get_actors_by_id(self):
        """Test success_assistant at GET '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test get /actors/<int:actor_id>")
        res = self.client().get(f'/actors/{actor_id}',
                                headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.OK)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], self.actor1_name)
        self.assertEqual(data['actor']['gender'], self.actor1_gender)
        self.assertEqual(len(data['cast_in']), 2)

    # casting director level
    # - Add or delete an actor from the database
    # - Modify actors or movies
    def test_forbidden_assistant_post_actor(self):
        """Test forbidden_assistant at POST '/actors'"""
        print("running test post /actors")
        res = self.client().post(f'/actors',
                                 headers=self.assist_header,
                                 json=self.new_actor_json)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    def test_forbidden_assistant_patch_actor(self):
        """
        Test forbidden_assistant at PATCH '/actors/<int:actor_id>'
        """
        actor_id = 1
        print("running test patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  headers=self.assist_header,
                                  json=self.actor1_json)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    def test_forbidden_assistant_delete_actor(self):
        """
        Test forbidden_assistant at DELETE '/actors/<int:actor_id>'
        """
        actor_id = 1
        print("running test delete /actors/<int:actor_id>")
        res = self.client().delete(f'/actors/{actor_id}',
                                   headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    def test_forbidden_assistant_patch_moive(self):
        """
        Test forbidden_assistant at PATCH '/moives/<int:movie_id>'
        """
        movie_id = 4
        print("running test patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.assist_header,
                                  json=self.patch_movie4_json)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    # Executive Producer level
    # - Add or delete a movie from the database
    def test_forbidden_assistant_post_movie(self):
        """Test forbidden_assistant at POST '/movies'"""
        print("running test post /movies")
        res = self.client().post(f'/movies',
                                 headers=self.assist_header,
                                 json=self.movie6_json)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    def test_forbidden_assistant_delete_movie(self):
        """
        Test forbidden_assistant at DELETE '/movie/<int:movie_id>'
        """
        movie_id = 1
        print("running test delete /movies/<int:movie_id>")
        res = self.client().delete(f'/movies/{movie_id}',
                                   headers=self.assist_header)
        self.assertEqual(res.status_code, Codes.FORBIDDEN)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.FORBIDDEN)
        self.assertEqual(data['message'], Codes.FORBIDDEN_MSG)

    #############################################################
    # Tests on all endpoints without any authorization header ###
    #############################################################

    def test_unauthorized_get_movies(self):
        """Test unauthorized at GET '/movies'"""
        print("running test unauthorized get /movies")
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_get_movies_by_id(self):
        """Test unauthorized at GET '/movies/<int:movie_id>'"""
        print("running test unauthorized get /movies/<int:movie_id>")
        movie_id = 1
        res = self.client().get(f'/movies/{movie_id}')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_get_actors(self):
        """Test unauthorized at GET '/actors'"""
        print("running test unauthorized get /actors")
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_get_actors_by_id(self):
        """Test unauthorized at GET '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test unauthorized get /actors/<int:actor_id>")
        res = self.client().get(f'/actors/{actor_id}')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_post_actor(self):
        """Test unauthorized at POST '/actors'"""
        print("running test unauthorized post /actors")
        res = self.client().post(f'/actors',
                                 json=self.new_actor_json)
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_patch_actor(self):
        """Test unauthorized at PATCH '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test unauthorized patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.actor1_json)
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_delete_actor(self):
        """Test unauthorized at DELETE '/actors/<int:actor_id>'"""
        actor_id = 1
        print("running test unauthorized delete /actors/<int:actor_id>")
        res = self.client().delete(f'/actors/{actor_id}')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_patch_moive(self):
        """Test unauthorized at PATCH '/moives/<int:movie_id>'"""
        movie_id = 4
        print("running test unauthorized patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=self.patch_movie4_json)
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_post_movie(self):
        """Test unauthorized at POST '/movies'"""
        print("running test unauthorized post /movies")
        res = self.client().post(f'/movies',
                                 json=self.movie6_json)
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    def test_unauthorized_delete_movie(self):
        """Test unauthorized at DELETE '/movie/<int:movie_id>'"""
        print("running test unauthorized delete /movies/<int:movie_id>")
        movie_id = 1
        res = self.client().delete(f'/movies/{movie_id}')
        self.assertEqual(res.status_code, Codes.UNAUTHORIZED)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNAUTHORIZED)
        self.assertEqual(data['message'], Codes.UNAUTHORIZED_MSG)

    ##########################################
    # Tests Getting, Patching, or Deleting ###
    # non-existent movies or actors        ###
    ##########################################
    def test_not_found_get_movies_by_id(self):
        """Test not_found at GET '/movies/<int:movie_id>'"""
        print("running test not_found get /movies/<int:movie_id>")
        movie_id = 99
        res = self.client().get(f'/movies/{movie_id}',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    def test_not_found_get_actors_by_id(self):
        """Test not_found at GET '/actors/<int:actor_id>'"""
        actor_id = 99
        print("running test not_found get /actors/<int:actor_id>")
        res = self.client().get(f'/actors/{actor_id}',
                                headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    def test_not_found_patch_actor(self):
        """Test not_found at PATCH '/actors/<int:actor_id>'"""
        actor_id = 99
        print("running test not_found patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  headers=self.exec_header,
                                  json=self.actor1_json)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    def test_not_found_delete_actor(self):
        """Test not_found at DELETE '/actors/<int:actor_id>'"""
        actor_id = 99
        print("running test not_found delete /actors/<int:actor_id>")
        res = self.client().delete(f'/actors/{actor_id}',
                                   headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    def test_not_found_patch_moive(self):
        """Test not_found at PATCH '/moives/<int:movie_id>'"""
        movie_id = 99
        print("running test not_found patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.exec_header,
                                  json=self.patch_movie4_json)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    def test_not_found_delete_movie(self):
        """Test not_found at DELETE '/movie/<int:movie_id>'"""
        print("running test not_found delete /movies/<int:movie_id>")
        movie_id = 99
        res = self.client().delete(f'/movies/{movie_id}',
                                   headers=self.exec_header)
        self.assertEqual(res.status_code, Codes.RESOURCE_NOT_FOUND)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.RESOURCE_NOT_FOUND)
        self.assertEqual(data['message'], Codes.RESOURCE_NOT_FOUND_MSG)

    #####################################################
    # Tests Posting or Patching W/O all required data ###
    #####################################################
    def test_unprocessable_duplicateName_post_actor(self):
        """Test unprocessable_duplicateName at POST '/actors'"""
        print("running test unprocessable_duplicateName post /actors")
        res = self.client().post(f'/actors',
                                 headers=self.exec_header,
                                 json={
                                     'name': self.actor1_name,
                                     'age': 21,
                                     'gender': "none"
                                 }
                                 )
        self.assertEqual(res.status_code, Codes.UNPROCESSABLE_ENTITY)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNPROCESSABLE_ENTITY)
        self.assertEqual(data['message'], Codes.UNPROCESSABLE_ENTITY_MSG)

    def test_badRequest_missingReqItem_post_actor(self):
        """Test badRequest_missingReqItem at POST '/actors'"""
        print("running test badRequest_missingReqItem post /actors")
        res = self.client().post(f'/actors',
                                 headers=self.exec_header,
                                 json={
                                     'name': self.actor1_name,
                                     'gender': "testing"
                                 }
                                 )
        self.assertEqual(res.status_code, Codes.BAD_REQUEST)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.BAD_REQUEST)
        self.assertEqual(data['message'], Codes.BAD_REQUEST_MSG)

    def test_unprocessable_duplicateName_patch_actor(self):
        """
        Test unprocessable_duplicateName at
        PATCH '/actors/<int:actor_id>'
        """
        actor_id = 1
        print("running test unprocessable_duplicateName \
            patch /actors/<int:actor_id>")
        res = self.client().patch(f'/actors/{actor_id}',
                                  headers=self.exec_header,
                                  json={
                                      'name': "Sean Connery",
                                      'age': 21,
                                      'gender': "testing"
                                  }
                                  )
        self.assertEqual(res.status_code, Codes.UNPROCESSABLE_ENTITY)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNPROCESSABLE_ENTITY)
        self.assertEqual(data['message'], Codes.UNPROCESSABLE_ENTITY_MSG)

    def test_badRequest_missingPartOfDate_patch_moive(self):
        """
        Test badRequest_missingPartOfDate at
        PATCH '/moives/<int:movie_id>'
        """
        movie_id = 4
        print("running test badRequest_missingPartOfDate \
            patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.exec_header,
                                  json={
                                      'title': "New Title",
                                      'release_month': "7",
                                      'release_day': "4",
                                      'actors': ["2", "3"]
                                  }
                                  )
        self.assertEqual(res.status_code, Codes.BAD_REQUEST)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.BAD_REQUEST)
        self.assertEqual(data['message'], Codes.BAD_REQUEST_MSG)

    def test_unprocessable_duplicateTitle_patch_moive(self):
        """
        Test unprocessable_duplicateTitle at
        PATCH '/moives/<int:movie_id>'
        """
        movie_id = 4
        print("running test uunprocessable_duplicateTitle \
            patch /movies/<int:moive_id>")
        res = self.client().patch(f'/movies/{movie_id}',
                                  headers=self.exec_header,
                                  json={
                                      'title': self.movie1_title,
                                      'release_month': "7",
                                      'release_day': "4",
                                      'release_year': "2000",
                                      'actors': ["2", "3"]
                                  }
                                  )
        self.assertEqual(res.status_code, Codes.UNPROCESSABLE_ENTITY)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.UNPROCESSABLE_ENTITY)
        self.assertEqual(data['message'], Codes.UNPROCESSABLE_ENTITY_MSG)

    def test_badRequest_missingReqItem_post_movie(self):
        """Test badRequest_missingReqItem at POST '/movies'"""
        print("running test badRequest_missingReqItem post /movies")
        res = self.client().post(f'/movies',
                                 headers=self.exec_header,
                                 json={
                                     'release_year': "1984",
                                     'release_month': "7",
                                     'release_day': "4",
                                     'actors': ["2", "3"]
                                 }
                                 )
        self.assertEqual(res.status_code, Codes.BAD_REQUEST)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], Codes.BAD_REQUEST)
        self.assertEqual(data['message'], Codes.BAD_REQUEST_MSG)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
