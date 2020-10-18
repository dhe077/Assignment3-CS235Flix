import pytest
# from CS235Flix.domainmodel.model import Movie, Actor, Review, Director, Genre, User

from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.watchlist import WatchList
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.user import User


class TestActorMethods:

    def test_init(self):
        actor1 = Actor("Angelina Jolie")
        print(actor1)
        actor2 = Actor("")
        print(actor2)
        actor3 = Actor(42)
        print(actor3)


class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None

    def test_lt(self):
        director1 = Director("Taika Waititi")
        director4 = Director("Spielberg")
        director_list = [director1, director4]
        director_list.sort()
        assert director_list[0] == director4 and director_list[1] == director1
        director5 = Director("Taika Zielberg")
        director_list2 = [director1, director5]
        director_list2.sort()
        assert director_list2[0] == director1 and director_list2[1] == director5
        director6 = Director("Taika")
        director_list3 = [director1, director6]
        director_list3.sort()
        assert director_list3[0] == director6 and director_list3[1] == director1

    def test_eq(self):
        director1 = Director("Cheesus")
        director2 = Director("Jeebus")
        director3 = Director("Cheesus")
        assert director1 != director2
        assert director1 == director3

    def test_hash(self):
        director1 = Director("Annabelle")
        hashed = hash(director1)
        assert director1.__hash__() == hashed

    def test_adding_directed_movie(self):
        pass


class TestReviewMethods:

    def test_init(self):
        movie = Movie("Moana", 2016, 1)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)

        print(review.movie)
        print("Review: {}".format(review.review_text))
        print("Rating: {}".format(review.rating))

        movie1 = ""
        review_text1 = ""
        rating1 = 0
        review1 = Review(movie1, review_text1, rating1)

        assert review1.rating is None
        assert review1.review_text is None
        movieEx = Movie("DEFAULT TITLE", 0, -1)
        print(movieEx)

    def test_repr(self):
        movie = Movie("Moana", 2016, 1)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        print()
        print(review)

    def test_eq(self):
        movie = Movie("Moana", 2016, 1)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        movie2 = Movie("Moana", 2016, 1)
        review_text2 = "This movie was very enjoyable."
        rating2 = 8
        review2 = Review(movie2, review_text2, rating2)
        assert review == review2
        movie3 = Movie("Moana", 2017, 2)
        review_text3 = "This movie was very enjoyable."
        rating3 = 8
        review3 = Review(movie3, review_text3, rating3)
        assert review != review3
        movie4 = Movie("", 0, -1)
        review_text4 = ""
        rating4 = 0
        review4 = Review(movie4, review_text4, rating4)
        assert review != review4

    def test_getters_setters(self):
        movie = Movie("Moana", 2016, 1)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)
        assert review.rating == 8
        assert review.movie == movie
        assert review.review_text == "This movie was very enjoyable."


class TestGenreMethods:

    def test_init(self):
        genre1 = Genre("Comedy")
        assert repr(genre1) == "<Genre Comedy>"
        genre2 = Genre("")
        assert genre2.genre_name is None
        genre3 = Genre(42)
        assert genre3.genre_name is None

    def test_lt(self):
        genre1 = Genre("Comedy")
        genre4 = Genre("Horror")
        genre_list = [genre4, genre1]
        genre_list.sort()
        assert genre_list[1] == genre4 and genre_list[0] == genre1
        genre5 = Genre("Comedian")
        genre_list2 = [genre1, genre5]
        genre_list2.sort()
        assert genre_list2[0] == genre5 and genre_list2[1] == genre1


class TestWatchlistMethods:

    def test_init(self):
        watchlist = WatchList()
        print()
        print(f"Size of watchlist: {watchlist.size()}")

    def test_add_movie(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Ice Age", 2002, 2))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3))
        print()
        print(watchlist.first_movie_in_watchlist())

    def test_check_size_of_nonempty_watchlist(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Ice Age", 2002, 2))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3))
        print()
        print(f"Size of watchlist is: {watchlist.size()}")

    def test_add_same_movie_again(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Moana", 2016, 2))
        print()
        print(f"Size of watchlist is: {watchlist.size()}")

    def test_remove_movie_which_is_not_in_watchlist(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.remove_movie(Movie("Ice Age", 2002, 2))
        print()
        print(f"Size of watchlist is: {watchlist.size()}")

    def test_remove_movie_which_is_in_watchlist(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.remove_movie(Movie("Moana", 2016, 2))
        print()
        print(f"Size of watchlist is: {watchlist.size()}")

    def test_select_movie_to_watch_index_ok(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Ice Age", 2002, 2))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3))
        print()
        print(f"Selected movie: {watchlist.select_movie_to_watch(0)}")

    def test_select_movie_to_watch_index_out_of_bounds(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Ice Age", 2002, 2))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3))
        print()
        print(f"Selected movie: {watchlist.select_movie_to_watch(9)}")

    def test_iterator_used(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016, 1))
        watchlist.add_movie(Movie("Ice Age", 2002, 2))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3))
        print()
        for movie in watchlist:
            print(movie)


class TestUserMethods:

    def test_init(self):
        user1 = User('Martin', 'pw12345')
        user2 = User('Ian', 'pw67890')
        user3 = User('Daniel', 'pw87465')
        print()
        print(user1)
        print(user2)
        print(user3)

    def test_hash(self):
        user1 = User('Martin', 'pw12345')
        user2 = User('Ian', 'pw67890')
        user3 = User('Daniel', 'pw87465')
        test_set = set()
        test_set.add(user1)
        test_set.add(user2)
        test_set.add(user3)
        print()
        print(test_set)

    def test_watch_movie(self):
        user1 = User('Martin', 'pw12345')
        user1.watch_movie(Movie("Moana", 2016, 1))
        print()
        print(user1.watched_movies)

        movies = [Movie("Moana", 2016, 1), Movie("Guardians of the Galaxy", 2014, 2)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        user = User("Martin", "pw12345")
        print(user.watched_movies)
        print(user.time_spent_watching_movies_minutes)
        for movie in movies:
            user.watch_movie(movie)
        print(user.watched_movies)
        print(user.time_spent_watching_movies_minutes)

    def test_add_review(self):
        user1 = User('Martin', 'pw12345')
        movie = Movie("Moana", 2016, 1)
        user1.add_review(Review(movie, "Ahhh", 2))
        print()
        print(user1.reviews)
        print(movie.external_rating)


class TestMovieMethods:

    def test_init(self):
        movie = Movie("Moana", 2016, 7)
        print(movie)

        director = Director("Ron Clements")
        movie.director = director
        print(movie.director)

        actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
        for actor in actors:
            movie.add_actor(actor)
        assert movie.actors == [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"),
                                Actor("Temuera Morrison")]
        assert len(movie.actors) == 4

        movie.runtime_minutes = 107
        print("Movie runtime: {} minutes".format(movie.runtime_minutes))

    def test_add_actor(self):
        movie = Movie("Moana", 2016, 1)
        movie.add_actor(Actor("Dwayne Johnson"))

        assert len(movie.actors) == 1
        assert movie.actors == [Actor("Dwayne Johnson")]

    def test_hash(self):
        movie1 = Movie("Moana1", 2016, 1)
        movie2 = Movie("Moana2", 2016, 2)
        movie3 = Movie("Moana3", 2016, 3)

        test_set = set()
        test_set.add(movie1)
        test_set.add(movie2)
        test_set.add(movie3)
        print()
        print(test_set)

    # extension test
    def test_add_rating_vote(self):
        movie = Movie("Moana", 2016, 7)
        movie.rating_votes = 5
        movie.external_rating = 6.2
        movie.add_rating_vote(8)
        print()
        print(f"Number of votes: {movie.rating_votes}")
        print(f"New rating for the movie: {movie.external_rating}")
        assert movie.external_rating == 6.5
        movie2 = Movie("ABC", 2016, 2)
        movie2.rating_votes = "2"
        movie2.external_rating = "2.5"
        movie2.add_rating_vote(10)
        assert movie2.external_rating == 5
        movie3 = Movie("", 0, 5)
        movie3.rating_votes = -1
        movie3.external_rating = "-2"
        movie3.add_rating_vote(10)
        assert movie3.external_rating == 10

    def test_revenue(self):
        movie = Movie("Moana", 2016, 7)
        movie.revenue = "23.6"
        assert movie.revenue == 23.6
        movie1 = Movie("Up", 2009, 8)
        movie1.revenue = "N/A"
        assert movie1.revenue is None
        movie2 = Movie("", 0, 1)
        movie2.revenue = 41.5
        assert movie2.revenue == 41.5
        movie3 = Movie("", 0, 1)
        movie3.revenue = -2
        assert movie3.revenue is None

    def test_metascores(self):
        movie = Movie("Moana", 2016, 7)
        movie.metascores = "23"
        assert movie.metascores == 23
        movie1 = Movie("Up", 2009, 8)
        movie1.revenue = "N/A"
        assert movie1.metascores is None
        movie2 = Movie("", 0, 1)
        movie2.metascores = 41
        assert movie2.metascores == 41
        movie3 = Movie("", 0, 1)
        movie3.metascores = -2
        assert movie3.metascores is None

    def test_ID(self):
        movie = Movie("Moana", 2016, 7)
        movie2 = Movie("Moana", 2016, 7)
        assert movie == movie2
        movie3 = Movie("Moana", 2016, 8)
        assert movie != movie3
