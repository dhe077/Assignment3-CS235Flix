import pytest
from CS235Flix.repositorydir.memory_repository import MemoryRepository
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.actor import Actor


def test_repository_can_add_user():
    mem_repo = MemoryRepository()
    user = User("Jimmy", "42069")
    mem_repo.add_user(user)

    assert mem_repo.get_user("Jimmy") is user


def test_repository_can_get_user():
    mem_repo = MemoryRepository()
    user = User("Terry", "42069")
    mem_repo.add_user(user)
    got_user = mem_repo.get_user("Terry")

    assert got_user == user


def test_repository_does_not_retrieve_a_non_existent_user():
    mem_repo = MemoryRepository()
    user = User("Bob", "42069")
    mem_repo.add_user(user)
    got_user = mem_repo.get_user("Terry")

    assert got_user is None


# movies
def test_repository_can_add_movie():
    mem_repo = MemoryRepository()
    movie = Movie("Up", 2009, 1)
    mem_repo.add_movie(movie)

    assert mem_repo.get_movie(1) is movie


def test_cannot_add_movie_with_non_unique_id():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 1)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)

    assert mem_repo.get_number_of_movies() == 1


def test_repository_can_add_movie_alhpa():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)

    assert mem_repo.get_number_of_movies() == 3
    assert mem_repo.get_first_movie() is dolittle_movie


def test_repository_can_retrieve_movie():
    mem_repo = MemoryRepository()
    movie = Movie("Up", 2009, 1)
    mem_repo.add_movie(movie)
    got_movie = mem_repo.get_movie(1)

    assert got_movie == movie


def test_repository_does_not_retrieve_a_non_existent_movie():
    mem_repo = MemoryRepository()
    movie = Movie("Up", 2009, 1)
    mem_repo.add_movie(movie)
    got_movie = mem_repo.get_movie(7)

    assert got_movie is None


def test_get_number_of_movies():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)

    assert mem_repo.get_number_of_movies() == 3


# movies by id
def test_repository_can_get_movies_by_id():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    movies_by_id = mem_repo.get_movies_by_id([1, 2, 3])

    assert len(movies_by_id) == 3
    assert movies_by_id == [up_movie, klaus_movie, dolittle_movie]


def test_repository_does_not_retrieve_a_non_existent_id():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_id = mem_repo.get_movies_by_id([1, 2, 4])

    assert len(movies_by_id) == 2
    assert movies_by_id == [up_movie, klaus_movie]


# movies by title
def test_repository_can_get_movies_by_title():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    movies_by_title = mem_repo.get_movies_by_title(["Up", "Klaus", "Dolittle"])

    assert len(movies_by_title) == 3
    assert movies_by_title == [up_movie, klaus_movie, dolittle_movie]


def test_repository_does_not_retrieve_a_non_existent_title():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_title = mem_repo.get_movies_by_title(["Up", "Klaus", "Frozen"])

    assert len(movies_by_title) == 2
    assert movies_by_title == [up_movie, klaus_movie]


# movies by director
def test_repository_can_get_movies_by_director():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    inside_out_movie = Movie("Inside Out", 2015, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.director = Director("Pete Docter")
    inside_out_movie.director = Director("Pete Docter")
    dolittle_movie.director = Director("Stephen Gaghan")
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(inside_out_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_director = mem_repo.get_movies_by_director(Director("Pete Docter"))

    assert len(movies_by_director) == 2
    assert movies_by_director == [inside_out_movie, up_movie]


def test_repository_does_not_retrieve_a_non_existent_director():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    inside_out_movie = Movie("Inside Out", 2015, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.director = Director("Pete Docter")
    inside_out_movie.director = Director("Pete Docter")
    dolittle_movie.director = Director("Stephen Gaghan")
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(inside_out_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_director = mem_repo.get_movies_by_director(Director("Sergio Pablos"))

    assert len(movies_by_director) == 0
    assert movies_by_director == []


# movies by genre
def test_repository_can_get_movies_by_genre():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    schindlers_list_movie = Movie("Schindler's List", 1993, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.add_genre(Genre("Comedy"))
    schindlers_list_movie.add_genre(Genre("War"))
    dolittle_movie.add_genre(Genre("Comedy"))
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(schindlers_list_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_genre = mem_repo.get_movies_by_genre(Genre("Comedy"))

    assert len(movies_by_genre) == 2
    assert movies_by_genre == [dolittle_movie, up_movie]


def test_repository_does_not_retrieve_a_non_existent_genre():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.add_genre(Genre("Comedy"))
    klaus_movie.add_genre(Genre("Comedy"))
    dolittle_movie.add_genre(Genre("Comedy"))
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_genre = mem_repo.get_movies_by_genre(Genre("War"))

    assert len(movies_by_genre) == 0
    assert movies_by_genre == []


# movies by actor
def test_repository_can_get_movies_by_actor():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    the_avengers_movie = Movie("The Avengers", 2012, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.add_actor(Actor("Ed Asner"))
    the_avengers_movie.add_actor(Actor("Robert Downey, Jr."))
    dolittle_movie.add_actor(Actor("Robert Downey, Jr."))
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(the_avengers_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_actor = mem_repo.get_movies_by_actor(Actor("Robert Downey, Jr."))

    assert len(movies_by_actor) == 2
    assert movies_by_actor == [dolittle_movie, the_avengers_movie]


def test_repository_does_not_retrieve_a_non_existent_actor():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    the_avengers_movie = Movie("The Avengers", 2012, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.add_actor(Actor("Ed Asner"))
    the_avengers_movie.add_actor(Actor("Robert Downey, Jr."))
    dolittle_movie.add_actor(Actor("Robert Downey, Jr."))
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(the_avengers_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_actor = mem_repo.get_movies_by_actor(Actor("Jim Carrey"))

    assert len(movies_by_actor) == 0
    assert movies_by_actor == []


# movies by high or low
def test_repository_can_get_movies_by_rating_high_to_low():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.external_rating = 89
    klaus_movie.external_rating = 90
    dolittle_movie.external_rating = 76
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_high_to_low = mem_repo.get_movies_by_rating_high()

    assert len(movies_by_high_to_low) == 3
    assert movies_by_high_to_low == [klaus_movie, up_movie, dolittle_movie]


def test_repository_can_get_movies_by_rating_low_to_high():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    up_movie.external_rating = 89
    klaus_movie.external_rating = 90
    dolittle_movie.external_rating = 76
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    movies_by_low_to_high = mem_repo.get_movies_by_rating_low()

    assert len(movies_by_low_to_high) == 3
    assert movies_by_low_to_high == [dolittle_movie, up_movie, klaus_movie]


def test_repository_returns_year_of_previous_movie():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    previous_year = mem_repo.get_year_of_previous_movie(klaus_movie)

    assert previous_year == 2009


def test_repository_returns_year_of_next_movie():
    mem_repo = MemoryRepository()
    up_movie = Movie("Up", 2009, 1)
    klaus_movie = Movie("Klaus", 2019, 2)
    dolittle_movie = Movie("Dolittle", 2019, 3)
    mem_repo.add_movie(up_movie)
    mem_repo.add_movie(klaus_movie)
    mem_repo.add_movie(dolittle_movie)
    # ["Dolittle", "Klaus", "Up"]
    next_year = mem_repo.get_year_of_next_movie(klaus_movie)

    assert next_year is None
