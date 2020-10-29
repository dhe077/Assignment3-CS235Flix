from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.review import Review


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password.strip()
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @user_name.setter
    def user_name(self, new_user_name: str):
        self.__user_name = new_user_name

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str):
        self.__password = new_password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @watched_movies.setter
    def watched_movies(self, new_watched_movies: list):
        self.__watched_movies = new_watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @reviews.setter
    def reviews(self, new_reviews: list):
        self.__reviews = new_reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, new_time: int):
        if new_time >= 0:
            self.__time_spent_watching_movies_minutes = new_time

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if self.__user_name == other.user_name:
            return True
        return False

    def __lt__(self, other):
        if self.__user_name < other.user_name:
            return True
        return False

    def __hash__(self):
        return hash(self.user_name)

    def watch_movie(self, movie: Movie):
        if type(movie) == Movie:
            self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    # extension method
    def add_review(self, review: Review):
        if type(review) == Review:
            self.__reviews.append(review)
        review.movie.add_rating_vote(review.rating)

    def user_getter(self):
        return self.__user_name
