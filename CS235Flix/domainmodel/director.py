
class Director:

    def __init__(self, director_full_name: str):
        from CS235Flix.domainmodel.movie import Movie
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self.__directed_movies = list()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @director_full_name.setter
    def director_full_name(self, new_name):
        self.__director_full_name = new_name

    @property
    def directed_movies(self):
        return self.__directed_movies

    @directed_movies.setter
    def directed_movies(self, new_movie_list):
        self.__directed_movies = new_movie_list

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

    def add_directed_movie(self, movie):
        self.__directed_movies.append(movie)
