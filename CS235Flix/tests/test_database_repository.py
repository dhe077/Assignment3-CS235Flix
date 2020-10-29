from datetime import date, datetime

import pytest

from CS235Flix.repositorydir.database_repository import SqlAlchemyRepository
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.review import Review
from CS235Flix.repositorydir.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    print()
    print(user, user2)
    assert user2 == user and user2 is user


def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 1000 movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movie_id = number_of_movies + 1

    movie = Movie("Up", 2009, new_movie_id)
    repo.add_movie(movie)

    retrieved = repo.get_movie(new_movie_id)
    assert retrieved is movie
    assert retrieved.title == movie.title
    assert retrieved.release_year == movie.release_year
    assert retrieved.ID == movie.ID
    assert retrieved.director == movie.director


def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"

    # Check that the omvie has the expecetd release_year.
    assert movie.release_year == 2014


def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(9999)
    assert movie is None


def test_repository_can_retrieve_movie_by_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_year(2014)

    # Check that the query returned 98 Articles.
    assert len(movies) == 98

    # these instructors are jokes...
    movies = repo.get_movies_by_year(2016)

    # Check that the query returned 5 Articles.
    assert len(movies) == 297


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_year(2077)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 10


def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_can_get_movies_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[0].title == 'Prometheus'
    assert movies[1].title == 'Suicide Squad'
    assert movies[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_movies_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 9999])

    assert len(movies) == 1
    assert movies[0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([0, 9999])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre("Action")

    assert movie_ids == [1, 2]


def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_year_of_previous_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(6)
    previous_year = repo.get_year_of_previous_movie(movie)

    assert previous_year == 2015


def test_repository_returns_none_when_there_are_no_previous_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(321)
    previous_year = repo.get_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_year_of_next_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)
    next_year = repo.get_year_of_next_movie(movie)

    assert next_year == 2015


def test_repository_returns_none_when_there_are_no_subsequent_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(3)
    next_year = repo.get_year_of_next_movie(movie)

    assert next_year is None


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motor Sports')
    repo.add_genre(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(4)
    review = Review(movie, "I hate singing!", 1)

    repo.add_review(review)

    assert review in repo.get_reviews()


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(4)
    review = Review(movie, "I hate singing!", 1)

    repo.add_review(review)

    assert len(repo.get_reviews()) == 1
