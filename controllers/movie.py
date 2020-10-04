from flask import jsonify, make_response

from ast import literal_eval
from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov  = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 400)

def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = "I`d must be integer"
            return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err),400)
        return make_response(jsonify(movie), 200)
    else:
        err = "No id specified"
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    try:
        data = get_request_data()
    except:
        data = {'name':'Fury','year':'2014','genre':'Action'}
    is_movie_exist = Movie.query.filter_by(name = data['name']).first()
    if is_movie_exist is not None:
        err = 'There are already a movie with name{}'.format(data['name'])
        return make_response(jsonify(error = err), 400)
    if data["name"].isalpha() and len(data["year"]) == 4 and data["genre"].isalpha():
        try:
            new_record = Movie.create(**data)
        except:
            err = 'Can not create such movie'
            return make_response(jsonify(error = err), 400)
    else:
        error = 'Something wrong with entered data'
        return make_response(jsonify(error = error), 400)
    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def update_movie():
    """
    Update movie record by id
    """
    try:
        data = get_request_data()
    except:
        data = {'id':6,'name':'Thor','year':'2011','genre':'Superhero movie'}
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id is not a integer'
            return make_response(jsonify(error = err), 400)
        is_movie_exist = Movie.query.filter_by(name = data['name'])
        if is_movie_exist is not None and is_movie_exist.id !=data['id']:
            err = 'Such movie is exist with another id'
            return make_response(jsonify(error = err), 400)
        if data["name"].isalpha() and len(data["year"]) == 4 and data["genre"].isalpha():
            try:
                upd_record = Movie.update(row_id,**data)
            except:
                err = 'Can`t update movie'
                return make_response(jsonify(error = err), 400)
        else:
            error = 'Someting wrong with your data'
            return make_response(jsonify(error = error), 400)
        upd_movie = {k:v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    else:
        err = 'No id'
        return make_response(jsonify(error = err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    try:
        data = get_request_data()
    except:
        data = {'id': 5}
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id is not a integer'
            return make_response(jsonify(error = err), 400)
        is_movie_exist = Movie.query.filter_by(id = row_id).first()
        if is_movie_exist is None:
            err = "There is no such movie"
            return make_response(jsonify(error = err), 400)
        else:
            Movie.delete(row_id)
            msg = "Record successfully deleted"
            return make_response(jsonify(message = msg), 200)
    else:
        err = "No id"
        return make_response(jsonify(error = err), 400)




def movie_add_relation():
    """
    Add actor to movie's cast
    """
    try:
        data = get_request_data()
    except:
        data = {'actor_id':11, 'movie_id': 5}
    if 'actor_id' in data.keys():
        try:
            actor_id = int(data['actor_id'])
        except:
            err = "actor_id must be an integer"
            return make_response(jsonify(error = err), 400)
    if 'movie_id' in data.keys:
        try:
            row_m_id = int(data['movie_id'])
        except:
            err = "Movie_id must be integer"
            return make_response(jsonify(error = err), 400)
    actor = Actor.query.filter_by(id = actor_id).first()
    if actor is None:
        err = "There are no such actor"
        return make_response(jsonify(error = err), 400)
    try:
        movie = Movie.add_relation(row_m_id,actor)
    except:
        err = 'Can not create relation'
        return make_response(jsonify(error = err), 400)
    rel_movie = {k:v for k,v in movie.__dict__.items() if k in MOVIE_FIELDS }
    rel_movie['actors'] = str(movie.actors)
    return make_response(jsonify(rel_movie), 200)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    try:
        data = get_request_data()
    except:
        data = {'movie_id': 6}
    if 'movie_id' in data.keys():
        try:
            movie_id = int(data['movie_id'])
        except:
            err = "id must an integer"
            return make_response(jsonify(error = err), 400)
        try:
            movie = Movie.clear_relations(movie_id)
        except:
            err = 'Cant clear relation'
            return make_response(jsonify(error = err), 400)
        rel_movie = {k:v for k,v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['actors'] = str(movie.actors)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No ID'
        return make_response(jsonify(error = err), 400)