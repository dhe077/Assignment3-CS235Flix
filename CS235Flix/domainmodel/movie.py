from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director


class Movie:

    def __init__(self, movie_name: str, year: int, id: int):
        from CS235Flix.domainmodel.review import Review
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
        if new_revenue is not None and new_revenue != "N/A":
            if float(new_revenue) >= 0:
                self.__revenue = float(new_revenue)

    @property
    def metascores(self) -> int:
        return self.__metascores

    @metascores.setter
    def metascores(self, new_metascores: int):
        if new_metascores is not None and new_metascores != "N/A":
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

    # extension method
    def add_rating_vote(self, rating: int):
        self.__rating_votes += 1
        self.__external_rating = (self.external_rating * (self.rating_votes - 1) + rating) / self.rating_votes

    def add_review(self, review):
        self.__reviews.append(review)