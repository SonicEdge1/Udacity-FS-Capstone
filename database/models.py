import os
from flask import Flask
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
import json
from sqlalchemy.orm import backref, relationship
from enum import Enum
from sqlalchemy.sql.sqltypes import Date

HEROKU_URI = os.getenv('HEROKU_URI')

migrate = Migrate()
db = SQLAlchemy()

database_port = "localhost:5432"
database_name = "casting"
database_path = "postgresql://{}:{}@{}/{}".format(
  'myuser',
  'mypass',
  database_port,
  database_name)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
# # remote db settings
# def setup_db(app, database_path=HEROKU_URI):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     # migrate.init_app(app, db)
#     Migrate(app, db)
#     # db.create_all()


# Local db settings
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)


actor_bookings = db.Table('actor_bookings',
                          db.Column(
                              'movie_id',
                              db.Integer,
                              db.ForeignKey('movies.id'),
                              primary_key=True),
                          db.Column(
                              'actor_id',
                              db.Integer,
                              db.ForeignKey('actors.id'),
                              primary_key=True)
                          )


'''
# Actor ######################################################
'''


class Actor(db.Model):
    '''
    Database model of an actor containing:
    id - Integer and unique identifier
    name - String of actor's name
    age - Integer of the actor's age
    gender - String of actor's gender
    '''
    __tablename__ = 'actors'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    age = Column(Integer(), nullable=False)
    gender = Column(String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    insert()
        inserts a new actor into a database
        the actor must have a unique name
        the actor must have a unique id or null id
        EXAMPLE
            actor =Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an actor from the database
        the actor must exist in the database
        EXAMPLE
            actor =Actor(name=req_name, age=req_age, gender=req_gender)
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an actor in the database
        the actor must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Casey Siemaszko'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    '''
    format()
        representation of the Actor model
    '''
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


'''
### Movie ########################################

'''


class Movie(db.Model):
    '''
    Database model of an Movie containing:
    id - Integer and unique identifier
    title - String of movie's title
    releaseDate - Date object of movie release date
    '''
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(180), unique=True, nullable=False)
    releaseDate = Column(Date(), nullable=False)
    actors = db.relationship('Actor', secondary=actor_bookings,
                             backref=db.backref('movies', lazy='dynamic'),
                             lazy='dynamic')

    def __init__(self, title, releaseDate, actors):
        self.title = title
        self.releaseDate = releaseDate
        self.actors = actors

    '''
    insert()
        inserts a new movie into the database
        the movie must have a unique title
        the movie must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, releaseDate=req_relaeseDate)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a move from the database
        the movie must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, releaseDate=req_releaseDate)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a movie in the database
        the movie must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Actor.id == id).one_or_none()
            movie.title = 'Three O'Clock High'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    '''
    format()
        representation of the Movie model
    '''
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate.isoformat(),
        }


'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
