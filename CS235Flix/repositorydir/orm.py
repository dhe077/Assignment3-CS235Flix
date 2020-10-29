from sqlalchemy import (
    Table, MetaData, Column, Integer, Float, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.user import User

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=True)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=True),
    Column('rating', Integer, nullable=True),
    Column('timestamp', Date, nullable=True),
    Column('user_id', Integer, ForeignKey('users.id'))
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('description', String(1024), nullable=True),

    Column('runtime_minutes', Integer, nullable=True),

    Column('external_rating', Float, nullable=True),
    Column('revenue', Float, nullable=True),
    Column('metascores', Integer, nullable=True),

    Column('director_name', ForeignKey('directors.id')),
    Column('actors_names', ForeignKey('actors.id')),
    Column('movie_genres', ForeignKey('genres.id'))
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(255))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String(255))
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255))
)


def map_model_to_tables():
    mapper(User, users, properties={
        '_User__user_name': users.c.user_name,
        '_User__password': users.c.password,
        '_User__time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_User__reviews': relationship(Review, backref='users')
    })
    mapper(Review, reviews, properties={
        '_Review__review_text': reviews.c.review_text,
        '_Review__rating': reviews.c.rating,
        '_Review__timestamp': reviews.c.timestamp
    })
    mapper(Movie, movies, properties={
        '_Movie__ID': movies.c.id,
        '_Movie__title': movies.c.title,
        '_Movie__release_year': movies.c.release_year,
        '_Movie__description': movies.c.description,
        '_Movie__runtime_minutes': movies.c.runtime_minutes,

        '_Movie__external_rating': movies.c.external_rating,
        '_Movie__revenue': movies.c.revenue,
        '_Movie__metascores': movies.c.metascores,

        '_Movie__director': relationship(Director, backref='movies'),
        '_Movie__actors': relationship(Actor, backref='movies'),
        '_Movie__genres': relationship(Genre, backref='movies')
    })
    mapper(Genre, genres, properties={
        '_Genre__genre_name': genres.c.genre_name
    })
    mapper(Director, directors, properties={
        '_Director__director_full_name': directors.c.director_full_name
    })
    mapper(Actor, actors, properties={
        '_Actor__actor_full_name': actors.c.actor_full_name
    })
