from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import CS235Flix.repositorydir.repository as repo
import CS235Flix.utilities.utilities as utilities
import CS235Flix.movies.services as services

from CS235Flix.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    # read query params
    target_year = request.args.get('release_year')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # fetch the first and last movies in the series
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_year is None:
        # no year query param, so return movies from year 1 of the series
        target_year = first_movie['release_year']

    if movie_to_show_reviews is None:
        # no view-reviews query parameter, so set to a non-existent movie id
        movie_to_show_reviews = -1
    else:
        # convert movie_to_show_reviews from str to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    # fetch movie(s) for the target year. this call also returns the previous and next years immediately
    # before and after the target year.
    movies, previous_year, next_year = services.get_movies_by_year(target_year, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # there's at least one movie for the target year
        if previous_year is not None:
            # there are movies on a previous year, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_year', year=previous_year)
            first_movie_url = url_for('movies_bp.movies_by_year', year=first_movie['release_year'])

        # there are movies on a subsequent year, so generate URLs for the 'next' and 'last' navigation buttons
        if next_year is not None:
            next_movie_url = url_for('movies_bp.movies_by_year', year=next_year)
            last_movie_url = url_for('movies_bp.movies_by_year', year=last_movie['release_year'])

        # construct urls for viewing movie reviews and adding reviews
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_year', year=target_year,
                                               view_reviews_for=movie['ID'])
            movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['ID'])

        # generate the webpage to display the movies
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title=target_year,
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # no movies to show, so return the homepage
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_tag', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # read query parameters
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # no view-reviews query param, so set to a non-existent movie ID
        movie_to_show_reviews = -1
    else:
        # convert movie_to_show_reviews from str to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # no cursor query param, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # convert cursor from string to int
        cursor = int(cursor)

    # retrieve movie ids for movies that have the genre with genre_name
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

    # retrieve the batch of movies to display on the web page
    movies = services.get_movies_by_ids(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # there are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # there are further movies, so generate URLs for the 'next' and 'last' navigation buttons
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # construct urls for views movie reviews and adding reviews
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                           view_reviews_for=movie['ID'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['ID'])

    # generate the webpage to display the movies
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies with the genre: ' + genre_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    # obatin the username of the currently logged in user
    username = session['username']

    # create form
    form = ReviewForm()

    if form.validate_on_submit():
        # successful POST
        # extract movie id
        movie_id = int(form.movie_id.data)

        # use the service layer to store the new review
        services.add_review(movie_id, form.review.data, username, 0, repo.repo_instance)

        # retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # cause the web browser to display the page of all movies that have the same date as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.movies_by_date', year=movie['release_year'], view_reviews_for=movie_id))

    if request.method == 'GET':
        # request is a HTTP GET to display the form
        # extract the movie
        movie_id = int(request.args.get('movie'))

        # store the movie id in the form
        form.movie_id.data = movie_id
    else:
        # request is a HTTP POST where for validation has failed.
        # extract the movie id of the movie being reviewed from the form
        movie_id = int(form.movie_id.data)

    # for a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a web page that allows
    # the user to enter a review. the generated web page includes a form object
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
