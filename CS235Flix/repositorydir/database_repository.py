import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.user import User
from CS235Flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.repositorydir.repository import AbstractRepository

genres = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie.ID == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        if target_year is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return movies matching target_date; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie.release_year == target_year).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie.ID)).first()
        return movie

    def get_movies_by_id(self, id_list):
        movies = self._session_cm.session.query(Movie).filter(Movie.ID.in_(id_list)).all()
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        movie_ids = []

        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table.
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE genre_name = :genre_name',
                                               {'genre_name': genre_name}).fetchone()

        if row is None:
            # No genre with the name genre_name - create an empty list.
            movie_ids = list()
        else:
            genre_id = row[0]

            # Retrieve article ids of movies associated with the genre.
            movie_ids = self._session_cm.session.execute(
                'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY movie_id ASC',
                {'genre_id': genre_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_movies_by_title(self, title_list: List[str]) -> List[Movie]:
        pass

    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        pass

    def get_movies_by_genre(self, target_genre: Genre) -> List[Movie]:
        pass

    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        pass

    def get_movies_by_rating_high(self) -> List[Movie]:
        pass

    def get_movies_by_rating_low(self) -> List[Movie]:
        pass

    def get_year_of_previous_movie(self, movie: Movie):
        result = None
        prev = self._session_cm.session.query(Movie).filter(Movie.release_year < movie.release_year).order_by(
            desc(Movie.release_year)).first()

        if prev is not None:
            result = prev.release_year

        return result

    def get_year_of_next_movie(self, movie: Movie):
        result = None
        next = self._session_cm.session.query(Movie).filter(Movie.release_year > movie.release_year).order_by(
            asc(Movie.release_year)).first()

        if next is not None:
            result = next.release_year

        return result

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews


def populate(session_factory, data_path):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()

    session = session_factory()
    # This takes all movies from the csv file (represented as domain model objects) and adds them to the
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!
    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)

    session.commit()


'''
def get_movie_data(movie_file_reader):
    movie_data = list()

    for movie in movie_file_reader.dataset_of_movies:
        data = (movie.ID, movie.title, movie.release_year)
        movie_data.append(data)

    return movie_data


def get_genre_data(movie_file_reader):
    genre_data = list()
    genre_key = 0

    for genre in movie_file_reader.dataset_of_genres:
        genre_key += 1
        data = (genre_key, genre.genre_name)
        genre_data.append(data)

    return genre_data


def get_movie_and_genre_ids(movie_file_reader):
    ids = list()
    genre_key = 0

    for movie in movie_file_reader.dataset_of_movies:
        data = (movie.ID, genre_key)
        ids.append(data)

    return ids


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()

    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    genres = dict()

    insert_movies = """
            INSERT INTO movies (
            ID, title, release_year)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movies, get_movie_data(movie_file_reader))

    insert_genres = """
            INSERT INTO genres (
            id, genre_name)
            VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_data(movie_file_reader))

    insert_movie_genres = """
            INSERT INTO movie_genres (
            id, movie_id, genre_id)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, get_movie_and_genre_ids(movie_file_reader))

    insert_users = """
            INSERT INTO users (
            id, username, password)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_review = """
            INSERT INTO reviews (
            id, movie_id, review_text, timestamp, rating)
            VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_review, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()
'''
