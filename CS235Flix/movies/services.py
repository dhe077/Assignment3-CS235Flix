from typing import List, Iterable

from CS235Flix.repositorydir.repository import AbstractRepository
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.user import User


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    # check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    review = Review(movie, review_text, rating, user)
    user.add_review(review)

    # update the repository
    repo.add_review(review)


def get_movie(movie_ID: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_ID)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_year(year, repo: AbstractRepository):
    movies = repo.get_movies_by_year(year)
    movies_dto = list()
    prev_year = next_year = None
    if len(movies) > 0:
        prev_year = repo.get_year_of_previous_movie(movies[0])
        next_year = repo.get_year_of_next_movie(movies[0])

        # convert movies to dict form
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)
    return movie_ids


def get_movies_by_ids(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    reviews = repo.get_reviews()
    matching_reviews = []
    for review in reviews:
        if review.movie.ID == movie.ID:
            matching_reviews.append(review)

    return reviews_to_dict(matching_reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    print()
    movie_dict = {
        'ID': movie.ID,
        'release_year': movie.release_year,
        'title': movie.title,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'runtime_minutes': movie.runtime_minutes,
        'description': movie.description,
        'external_rating': movie.external_rating,
        'rating_votes': movie.rating_votes,
        'revenue': movie.revenue,
        'metascores': movie.metascores
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'movie_id': review.movie.ID,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_related_movies': [movie.ID for movie in genre.related_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dictn):
    movie = Movie(dictn[title], dictn.release_year, dictn[ID])
    return movie
