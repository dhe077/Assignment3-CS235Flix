import csv
import os

from CS235Flix.domainmodel.user import User


class UserFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = os.path.join(file_name, 'users.csv')
        self.__dataset_of_users = []

    @property
    def dataset_of_users(self):
        return self.__dataset_of_users

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            user_file_reader = csv.DictReader(csvfile)

            for row in user_file_reader:
                id = row['id']
                user_name = row['user_name']
                password = row['password']

                user = User(user_name, password)
                self.__dataset_of_users.append(user)
