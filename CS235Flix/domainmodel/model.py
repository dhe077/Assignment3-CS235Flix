from datetime import date, datetime
from typing import List, Iterable


class Actor:

    def __init__(self, actor_name: str):
        if actor_name == "" or type(actor_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_name.strip()
        self.colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if self.actor_full_name == other.actor_full_name:
            return True
        return False

    def __lt__(self, other):
        if self.actor_full_name < other.actor_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague):
        self.colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.colleagues:
            return True
        return False


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @director_full_name.setter
    def director_full_name(self, new_name):
        self.__director_full_name = new_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if self.director_full_name == other.director_full_name:
            return True
        return False

    def __lt__(self, other):
        if self.director_full_name < other.director_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.director_full_name)


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()
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
    def time_spent_watching_movies(self, new_time: int):
        if new_time >= 0:
            self.__time_spent_watching_movies_minutes = new_time

    def __repr__(self):
        return f"<User {self.user_name}>"

    def __eq__(self, other):
        if self.user_name == other.user_name:
            return True
        return False

    def __lt__(self, other):
        if self.user_name < other.user_name:
            return True
        return False

    def __hash__(self):
        return hash(self.user_name)

    # extension method
    def add_review(self, review: Review):
        if type(review) == Review:
            self.__reviews.append(review)
        review.movie.add_rating_vote(review.rating)


class Review:

    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) == Movie:
            self.__movie = movie
        else:
            self.__movie = Movie("DEFAULT TITLE", 0)
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()
        if 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.today()
        self.__user: User = None

    @property
    def movie(self) -> Movie:
        return self.__movie

    @movie.setter
    def movie(self, new_movie: Movie):
        self.__movie = new_movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @review_text.setter
    def review_text(self, new_review_text):
        self.__review_text = new_review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, new_rating):
        self.__rating = new_rating

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp):
        self.__timestamp = new_timestamp

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, new_user):
        self.__user = new_user

    def __repr__(self):
        return f"<Review {self.__movie}, {self.__timestamp}>"

    def __eq__(self, other):
        if self.movie == other.movie and self.rating == other.rating and \
                self.review_text == other.review_text and self.timestamp == other.timestamp:
            return True
        return False


class Movie:

    def __init__(self, movie_name: str, year: int, id: int):
        if movie_name == "" or type(movie_name) is not str:
            self.__title = None
        else:
            self.__title = movie_name.strip()
        if year >= 1900:
            self.__release_year = year
        else:
            self.__release_year = None
        self.__description: str = ""
        self.__director: Director = None
        self.__actors: list = list()
        self.__genres: list = list()
        self.__runtime_minutes: int = 0

        self.__external_rating = 0
        self.__rating_votes = 0
        self.__revenue = None
        self.__metascores = None

        self.__ID: int = id
        self.__reviews = list()

    # property mechanism of title, description, director, actors, genres,
    # runtime, external_rating, revenue and metascores
    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        self.__title = new_title

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new_description: str):
        self.__description = new_description

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, new_director: Director):
        self.__director = new_director

    @property
    def actors(self) -> list:
        return self.__actors

    @actors.setter
    def actors(self, new_actors_list: list):
        self.__actors = new_actors_list

    @property
    def genres(self) -> list:
        return self.__genres

    @genres.setter
    def genres(self, new_genres_list: list):
        self.__genres = new_genres_list

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime_minutes):
        if new_runtime_minutes > 0:
            self.__runtime_minutes = new_runtime_minutes
        else:
            raise ValueError

    # extensions properties below
    @property
    def external_rating(self) -> float:
        return self.__external_rating

    @external_rating.setter
    def external_rating(self, new_external_rating: float):
        if new_external_rating is not float:
            if float(new_external_rating) >= 0:
                self.__external_rating = float(new_external_rating)

    @property
    def rating_votes(self) -> int:
        return self.__rating_votes

    @rating_votes.setter
    def rating_votes(self, new_rating_votes: int):
        if new_rating_votes is not int:
            if int(new_rating_votes) >= 0:
                self.__rating_votes = int(new_rating_votes)

    @property
    def revenue(self) -> int:
        return self.__revenue

    @revenue.setter
    def revenue(self, new_revenue: float):
        if new_revenue is not float and new_revenue != "N/A":
            if float(new_revenue) >= 0:
                self.__revenue = float(new_revenue)

    @property
    def metascores(self) -> int:
        return self.__metascores

    @metascores.setter
    def metascores(self, new_metascores: int):
        if new_metascores is not int and new_metascores != "N/A":
            if int(new_metascores) >= 0:
                self.__metascores = int(new_metascores)

    @property
    def ID(self) -> int:
        return self.__ID

    @ID.setter
    def ID(self, new_ID: int):
        self.__ID = new_ID

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, new_release_year: int):
        self.__release_year = new_release_year

    @property
    def reviews(self) -> list:
        return self.__reviews

    def reviews(self, new_review_list):
        self.__reviews = new_review_list

    # add external rating, rating votes, revenue and meta scores as extra

    def __repr__(self) -> str:
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if self.__title == other.title and self.__release_year == other.__release_year and self.__ID == other.__ID:
            return True
        return False

    def __lt__(self, other):
        if self.title < other.title:
            return True
        return False

    def __hash__(self):
        return hash(self.title)

    def add_actor(self, actor: Actor):
        if actor not in self.__actors:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre):
        if genre not in self.__genres:
            self.__genres.append(genre)
            genre.add_related_movie(self)

    def remove_genre(self, genre: Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)
            genre.remove_related_movie(self)

    # extension method
    def add_rating_vote(self, rating: int):
        self.__rating_votes += 1
        self.__external_rating = (self.external_rating * (self.rating_votes - 1) + rating) / self.rating_votes

    def add_review(self, new_review: Review):
        if new_review.movie.ID == self.__ID:
            self.__reviews.append(new_review)


class Genre:

    def __init__(self, genre: str):
        if genre == "" or type(genre) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre.strip()
        self.__related_movies = list()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def related_movies(self) -> list:
        return self.__related_movies

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if self.genre_name == other.genre_name:
            return True
        return False

    def __lt__(self, other):
        if self.genre_name < other.genre_name:
            return True
        return False

    def __hash__(self):
        return hash(self.genre_name)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__related_movies

    def add_related_movie(self, movie: Movie):
        self.__related_movies.append(movie)


class ModelException(Exception):
    pass


def make_review(review_text: str, user: User, movie: Movie, rating: int):
    review = Review(movie, review_text, rating)
    user.add_review(review)
    movie.add_review(review)
    return review


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Tag {genre.genre_name} already applied to Movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_related_movie(movie)


def watch_movie(user: User, movie: Movie):
    if type(movie) == Movie:
        user.watched_movies.append(movie)
    user.time_spent_watching_movies_minutes += movie.runtime_minutes
