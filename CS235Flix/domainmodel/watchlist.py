from CS235Flix.domainmodel.movie import Movie


class WatchList:

    def __init__(self):
        self.__movie_watchlist = []
        self.__index = 0

    @property
    def movie_watchlist(self) -> list:
        return self.__movie_watchlist

    @movie_watchlist.setter
    def movie_watchlist(self, new_watchlist: list):
        self.__movie_watchlist = new_watchlist

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index >= len(self.movie_watchlist):
            self.__index = 0
            raise StopIteration
        self.__index += 1
        return self.__movie_watchlist[self.__index - 1]

    def add_movie(self, movie: Movie):
        if type(movie) == Movie:
            if movie not in self.__movie_watchlist:
                self.__movie_watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if type(movie) == Movie:
            if movie in self.__movie_watchlist:
                self.__movie_watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if 0 <= index < len(self.__movie_watchlist):
            return self.__movie_watchlist[index]
        return None

    def size(self):
        return len(self.movie_watchlist)

    def first_movie_in_watchlist(self):
        if self.size() >= 1:
            return self.movie_watchlist[0]
        return None
