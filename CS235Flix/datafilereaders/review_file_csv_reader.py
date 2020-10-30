import csv
import os

from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User


class ReviewFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = os.path.join(file_name, 'reviews.csv')
        self.__dataset_of_reviews = []

    @property
    def dataset_of_reviews(self):
        return self.__dataset_of_reviews

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            review_file_reader = csv.DictReader(csvfile)

            for row in review_file_reader:
                id = row['id']
                movie_info = row['movie-info']
                review_text = row['review-text']
                rating = row['rating']
                user_info = row['user-info']

                movie_info = movie_info.split(", ")
                user_info = user_info.split(", ")
                movie = Movie(movie_info[0], int(movie_info[1]), movie_info[2])
                user = User(user_info[0], user_info[1])
                review = Review(movie, review_text, int(rating), user)

                self.__dataset_of_reviews.append(review)
