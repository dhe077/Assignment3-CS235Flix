import abc
from typing import List
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.review import Review


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repositroy. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.
            If there is no User with the given username, this method returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title) -> Movie:
        """ Returns the Movie named title from the repository.
            If there is no Movie with the given title, this method returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        """ Returns a list of Movies that were published on the target_year.
            If there are no Movies for the given target_year, this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie in the repository.
            Returns None if the repository is empty. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie in the repository.
            Returns None if the repository is empty. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, ID_list: List[int]) -> List[Movie]:
        """ Returns a list of Movies, whose ID matches the IDs in the ID_list, in the repository.
            If there are no matches, this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Movies that have the genres in genre_name.
            If there are no movies that have genre_name, this method returns an empty list."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_title(self, title_list: List[str]) -> List[Movie]:
        """ Returns a list of Movies, whose titles match those in the title_list, from the repository.
            If there are no matches, this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        """ Returns a list of Movies, that have been directed by the target_director, from the repository.
            If there are no movies directed by the given target_director then this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, target_genre: Genre) -> List[Movie]:
        """ Returns a list of Movies, that have the same Genre as the target_genre, from the repository.
            If there are no movies of the target_genre then this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        """ Returns a list of Movies, that have the same Actor as the target_actor, from the repository.
            If there are no movies with the target_actor then this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rating_high(self) -> List[Movie]:
        """ Returns a list of Movie, from high to low rating, from the repository.
            If there are no Movies in the repository then this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rating_low(self) -> List[Movie]:
        """ Returns a list of Movie, from low to high rating, from the repository.
            If there are no Movies in the repository then this method returns an empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_previous_movie(self, movie: Movie):
        """ Returns the release year of the Movie that immediately precedes movie.
            If movie is the first Movie in the repository, this method returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_next_movie(self, movie: Movie):
        """ Returns the release year of the Movie that immediately follows movie.
            If movie is the first Movie in the repository, this method returns None. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError
