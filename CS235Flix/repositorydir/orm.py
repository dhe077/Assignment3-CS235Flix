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
    Column('time_spent_watching_movies_minutes', Integer)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=True),
    Column('rating', Integer, nullable=False),
    Column('timestamp', Date, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'))
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('description', String(1024), nullable=True),

    Column('runtime_minutes', Integer, nullable=True),

    Column('external_rating', Float, nullable=True),
    Column('revenue', Float, nullable=True),
    Column('metascores', Integer, nullable=True),

    Column('director_id', ForeignKey('directors.id'), nullable=True)
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
        '__user_name': users.c.user_name,
        '__password': users.c.password,
        '__time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '__reviews': relationship(Review, backref='users')
    })
    mapper(Review, reviews, properties={
        '__review_text': reviews.c.review_text,
        '__rating': reviews.c.rating,
        '__timestamp': reviews.c.timestamp
    })
    mapper(Movie, movies, properties={
        'ID': movies.c.id,
        '__title': movies.c.title,
        'release_year': movies.c.release_year,
        '__description': movies.c.description,
        'runtime_minutes': movies.c.runtime_minutes,

        'external_rating': movies.c.external_rating,
        'revenue': movies.c.revenue,
        'metascores': movies.c.metascores
    })
    mapper(Genre, genres, properties={
        '__genre_name': genres.c.genre_name
    })
    mapper(Director, directors, properties={
        '__director_full_name': directors.c.director_full_name
    })
