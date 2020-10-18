from typing import List
from bisect import bisect, bisect_left, insort_left

from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.review import Review
from CS235Flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.repositorydir.repository import AbstractRepository, RepositoryException


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._movies_ids = dict()
        self._users = list()
        self._reviews = list()
        self._genres = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username):
        for user in self._users:
            if user.user_name == username:
                return user

    def add_movie(self, movie: Movie):
        if movie.ID not in self._movies_ids:
            insort_left(self._movies, movie)
            self._movies_ids[movie.ID] = movie
        else:
            pass

    def get_movie(self, id):
        movie = None
        try:
            movie = self._movies_ids[id]
        except KeyError:
            pass
        return movie

    def get_movies_by_year(self, target_year):
        matching_movies = list()
        for movie in self._movies:
            if movie.release_year == target_year:
                insort_left(matching_movies, movie)
        return matching_movies

    def get_number_of_movies(self) -> int:
        return len(self._movies)

    def get_first_movie(self) -> Movie:
        return self._movies[0]

    def get_last_movie(self) -> Movie:
        return self._movies[-1]

    def get_movies_by_id(self, ID_list: List[int]):
        movies_by_id = list()
        for id in ID_list:
            for movie in self._movies:
                if movie.ID == id:
                    movies_by_id.append(movie)
        return movies_by_id

    def get_movie_ids_for_genre(self, genre_name: str):
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        if genre is not None:
            movie_ids = [movie.ID for movie in genre.related_movies]
        else:
            movie_ids = list()
        return movie_ids

    def get_movies_by_title(self, keyword: List[str]) -> List[Movie]:
        movies_by_title = list()
        for title in keyword:
            for movie in self._movies:
                if movie.title == title:
                    movies_by_title.append(movie)
        return movies_by_title

    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        movies_by_director = list()
        for movie in self._movies:
            if movie.director == target_director:
                movies_by_director.append(movie)
        return movies_by_director

    def get_movies_by_genre(self, target_genre: Genre) -> List[Movie]:
        movies_by_genre = list()
        for movie in self._movies:
            if target_genre in movie.genres:
                movies_by_genre.append(movie)
        return movies_by_genre

    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        movies_by_actor = list()
        for movie in self._movies:
            if target_actor in movie.actors:
                movies_by_actor.append(movie)
        return movies_by_actor

    def get_movies_by_rating_high(self) -> List[Movie]:
        high_to_low_movies = list()
        # find the highest rating movie then work your way down to the lowest
        visited = []
        index = 0
        while len(visited) != len(self._movies):
            highest = None
            for i in range(len(self._movies)):
                if i not in visited:
                    if highest is None or self._movies[i].external_rating > highest.external_rating:
                        highest = self._movies[i]
                        index = i
            if index not in visited:
                visited.append(index)
                high_to_low_movies.append(highest)
        return high_to_low_movies

    def get_movies_by_rating_low(self) -> List[Movie]:
        low_to_high_movies = list()
        # find the lowest rating movie then work your way up to the highest
        visited = []
        index = 0
        while len(visited) != len(self._movies):
            lowest = None
            for i in range(len(self._movies)):
                if i not in visited:
                    if lowest is None or self._movies[i].external_rating < lowest.external_rating:
                        lowest = self._movies[i]
                        index = i
            if index not in visited:
                visited.append(index)
                low_to_high_movies.append(lowest)
        return low_to_high_movies

    def get_year_of_previous_movie(self, movie: Movie):
        previous_year = None
        previous_year_list = list()
        if self.movie_index(movie) < len(self._movies):
            for search_movie in self._movies:
                if search_movie.release_year < movie.release_year and search_movie.ID != movie.ID:
                    insort_left(previous_year_list, search_movie.release_year)
            if len(previous_year_list) > 0:
                previous_year = previous_year_list[-1]
        return previous_year

    def get_year_of_next_movie(self, movie: Movie):  # alphabetically
        next_year = None
        next_year_list = list()
        if self.movie_index(movie) < len(self._movies):
            for search_movie in self._movies:
                if search_movie.release_year > movie.release_year and search_movie.ID != movie.ID:
                    insort_left(next_year_list, search_movie.release_year)
            if len(next_year_list) > 0:
                next_year = next_year_list[0]
        return next_year

    def add_genre(self, genre: Genre):
        if genre not in self._reviews:
            self._reviews.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._reviews

    def add_review(self, review: Review):
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].ID == movie.ID:
            return index
        raise ValueError


def populate(data_path: str, repo: AbstractRepository):
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)
    for genre in movie_file_reader.dataset_of_genres:
        repo.add_genre(genre)

