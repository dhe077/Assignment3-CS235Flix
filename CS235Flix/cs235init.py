from CS235Flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.domainmodel.user import User, Review, Movie


def main():
    filename = 'datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    print(f'number of unique movies: {len(movie_file_reader.dataset_of_movies)}')
    print(f'number of unique actors: {len(movie_file_reader.dataset_of_actors)}')
    print(f'number of unique directors: {len(movie_file_reader.dataset_of_directors)}')
    print(f'number of unique genres: {len(movie_file_reader.dataset_of_genres)}')
    assert len(movie_file_reader.dataset_of_movies) == 1000
    assert len(movie_file_reader.dataset_of_actors) == 1985
    assert len(movie_file_reader.dataset_of_directors) == 644
    assert len(movie_file_reader.dataset_of_genres) == 20

    all_directors_sorted = sorted(movie_file_reader.dataset_of_directors)
    assert str(
        all_directors_sorted[0:3]) == "[<Director Aamir Khan>, <Director Abdellatif Kechiche>, <Director Adam Leon>]"

    all_actors_sorted = sorted(movie_file_reader.dataset_of_actors)
    print(all_actors_sorted[0:3])

    # extension testing
    assert movie_file_reader.dataset_of_movies[0].external_rating == 8.1
    assert movie_file_reader.dataset_of_movies[0].rating_votes == 757074
    assert movie_file_reader.dataset_of_movies[0].revenue == 333.13
    assert movie_file_reader.dataset_of_movies[0].metascores == 76


if __name__ == "__main__":
    main()
