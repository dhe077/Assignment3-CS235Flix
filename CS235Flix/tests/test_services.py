import pytest

from CS235Flix.repositorydir.memory_repository import MemoryRepository
from CS235Flix.movies.services import NonExistentMovieException
from CS235Flix.authentication.services import AuthenticationException
from CS235Flix.movies import services as movie_services
from CS235Flix.authentication import services as auth_services
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
# from CS235Flix.domainmodel.model import Movie, Actor, Review, Director, Genre, User


def test_can_add_user():
    mem_repo = MemoryRepository()
    new_user_name = "kelly007"
    new_password = "abcd1A23"
    auth_services.add_user(new_user_name, new_password, mem_repo)
    user_as_dict = auth_services.get_user(new_user_name, mem_repo)
    assert user_as_dict["username"] == new_user_name

    # check that password has been encrypted.
    assert user_as_dict["password"].startswith("pbkdf2:sha256:")


def test_cannot_add_user_with_existing_name():
    mem_repo = MemoryRepository()
    user_name = "annab3ll3"
    password = "imcool123"
    auth_services.add_user(user_name, password, mem_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, mem_repo)


def test_authentication_with_valid_credentials():
    mem_repo = MemoryRepository()
    new_user_name = "ecartman"
    new_password = "abcd1A23"
    auth_services.add_user(new_user_name, new_password, mem_repo)
    try:
        auth_services.authenticate_user(new_user_name, new_password, mem_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials():
    mem_repo = MemoryRepository()
    new_user_name = "lumehtial"
    new_password = "abcd1A23"
    auth_services.add_user(new_user_name, new_password, mem_repo)
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', mem_repo)


def test_can_add_review():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    movie_id = 3
    review_text = "Very good!"
    username = "jumanji"
    rating = 5
    mem_repo.add_user(User(username, "CS235"))

    # call the service layer to add the comment
    movie_services.add_review(movie_id, review_text, rating, username, mem_repo)

    # retrieve the reviews for the movie from the repository
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, mem_repo)

    # check that the reviews inclue a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_can_get_movie():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    movie_id = 2
    movie_as_dict = movie_services.get_movie(movie_id, mem_repo)

    assert movie_as_dict["ID"] == movie_id
    assert movie_as_dict["release_year"] == klaus_movie.release_year
    assert movie_as_dict["title"] == "Klaus"


def test_cannot_get_movie_with_non_existent_id():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    movie_id = 7

    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie(movie_id, mem_repo)


def test_get_first_movie():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movie_as_dict = movie_services.get_first_movie(mem_repo)
    # ["Dolittle", "Klaus", "Up"]

    assert movie_as_dict["ID"] == 3


def test_get_last_movie():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movie_as_dict = movie_services.get_last_movie(mem_repo)
    # ["Dolittle", "Klaus", "Up"]

    assert movie_as_dict["ID"] == 1


def test_get_movies_by_year_with_one_year():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)

    target_year = 2009
    movies_as_dict, prev_date, next_date = movie_services.get_movies_by_year(target_year, mem_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]["ID"] == 1

    assert prev_date is None
    assert next_date == 2019


def test_get_movies_by_year_with_multiple_years():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    sonic_movie = Movie("Sonic the Hedgehog", 2020, 4)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    mem_repo.add_movie(sonic_movie)

    target_year = 2019
    movies_as_dict, prev_date, next_date = movie_services.get_movies_by_year(target_year, mem_repo)

    assert len(movies_as_dict) == 2
    movie_ids = [movie["ID"] for movie in movies_as_dict]
    assert {2, 3}.issubset(movie_ids)

    assert prev_date == 2009
    assert next_date == 2020


def test_get_movies_by_year_with_non_existent_date():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)

    target_year = 2020
    movies_as_dict, prev_date, next_date = movie_services.get_movies_by_year(target_year, mem_repo)

    assert len(movies_as_dict) == 0


def test_get_movies_by_id():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)

    target_movie_ids = [2, 1, 4, 5]
    movies_as_dict = movie_services.get_movies_by_ids(target_movie_ids, mem_repo)

    # check that 2 movies were returned from the query
    assert len(movies_as_dict) == 2

    # check that the movie ids returned were 1 and 2
    movie_ids = [movie["ID"] for movie in movies_as_dict]
    assert {1, 2}.issubset(movie_ids)
