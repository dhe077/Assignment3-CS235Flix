import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.review import Review


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (ID, title, release_year, description, runtime_minutes) VALUES '
        '(:ID, "Up", "2009", "", 120)'
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Sports", "New Zealand")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie_genre_associations(empty_session, movie_key, genre_keys):
    stmt = 'INSERT INTO movie_tags (movie_ID, genre_id) VALUES (:movie_ID, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'movie_ID': movie_key, 'genre_id': genre_key})


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO comments (user_id, movie_id, comment, timestamp) VALUES '
        '(:user_id, :movie_ID, "Comment 1", :timestamp_1),'
        '(:user_id, :movie_ID, "Comment 2", :timestamp_2)',
        {'user_id': user_key, 'movie_ID': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    article = Article("Up", 2009, 1)
    return article


def make_user():
    user = User("Andrew", "111")
    return user


def make_genre():
    genre = Genre("New Zealand")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]

    assert empty_session.query(User).all() == expected
