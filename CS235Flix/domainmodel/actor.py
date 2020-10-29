
class Actor:

    def __init__(self, actor_name: str):
        from CS235Flix.domainmodel.movie import Movie
        if actor_name == "" or type(actor_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_name.strip()
        self.colleagues = []
        self.__movies_acted_in = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def movies_acted_in(self):
        return self.__movies_acted_in

    @movies_acted_in.setter
    def movies_acted_in(self, new_movie_list):
        self.__movies_acted_in = new_movie_list

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

    def add_movie_acted_in(self, movie):
        self.__movies_acted_in.append(movie)
