from datetime import date, datetime

import pytest

from CS235Flix.repositorydir.database_repository import SqlAlchemyRepository
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.review import Review
from CS235Flix.repositorydir.repository import RepositoryException


def test_users():
    user = User('Dave', '123456789')
    assert user.user_name == 'Dave'
    assert user.password == '123456789'


def test_movies(session_factory):
    movie = Movie("Up", 2009, 1)
    print()
    print(movie, movie.title, movie.release_year)


def test_repository_can_add_a_user(session_factory):
    print()
    print("Starting")
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    print("Created user {}".format(user.user_name))

    repo.add_user(user)
    print("Added user")

    user2 = User('Martin', '123456789')

    repo.add_user(user2)

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user
    print("finished assert")


def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 1000 movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movie_id = number_of_movies + 1

    movie = Movie("Up", 2009, number_of_movies)
    repo.add_movie(movie)

    assert repo.get_movie(new_movie_id) == movie


def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the movie has the expected title.
    print(movie.title)
