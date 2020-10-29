from datetime import datetime

from CS235Flix.domainmodel.movie import Movie


class Review:

    def __init__(self, movie: Movie, review_text: str, rating: int, user):
        from CS235Flix.domainmodel.user import User
        if type(movie) == Movie:
            self.__movie = movie
        else:
            self.__movie = Movie("DEFAULT TITLE", 0, -1)
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()
        if 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.today()

        self.__user: User = user
        self.__movie.add_review(self)

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
    def user(self):
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


