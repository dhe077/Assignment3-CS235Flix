
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

    def is_applied_to(self, movie) -> bool:
        return movie in self.__related_movies

    def add_related_movie(self, movie):
        self.__related_movies.append(movie)


