from sqlalchemy import select, inspect

import pytest

from CS235Flix.repositorydir.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors', 'directors', 'genres', 'movie_genres', 'movies', 'reviews', 'users']


def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert len(all_genre_names) == 2555
        print()
        print(all_genre_names)


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']


def test_database_populate_select_all_movies(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []
        for row in result:
            all_movies.append((row['id'], row['title']))

        print()
        print(all_movies)
        assert len(all_movies) == 1000
