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


migrate = Migrate()

project_dir = os.path.dirname(os.path.abspath(__file__))
# database_filename = "database.db"

Heroku_Host = "ec2-52-1-20-236.compute-1.amazonaws.com:5432"
Heroku_DBname = "d23cmcbfab52ss"
Heroku_User = "xibzplxukrsyqb"
Heroku_Password = "ac5916d7271da41c21c3695491e47d3595ba31c5a1ee644413715e097320bfdb"
Heroku_URI = "sqlite://xibzplxukrsyqb:ac5916d7271da41c21c3695491e47d3595ba31c5a1ee644413715e097320bfdb@ec2-52-1-20-236.compute-1.amazonaws.com:5432/d23cmcbfab52ss"

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=Heroku_URI):
#     database_path = "sqlite:///{}".format(
#        Heroku_User,
#        Heroku_Password,
#        Heroku_Host,
#        Heroku_DBname
#    )
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # migrate.init_app(app, db)
    Migrate(app, db)
    # db.create_all()

## Local db settings
# def setup_db(app, database_filename=database_filename):
#     database_path = "sqlite:///{}".format(
#         os.path.join(project_dir, database_filename))
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     # migrate.init_app(app, db)
#     Migrate(app, db)
#     # db.create_all()


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

    # Autoincrementing, unique primary key
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
