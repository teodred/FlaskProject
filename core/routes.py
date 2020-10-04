from flask import Flask, request
from flask import current_app as app

from controllers.actor import *
from controllers.movie import *


@app.route('/api/actors', methods=['GET'])
def actors():
    """
    Get all actors in db
    """
    return get_all_actors()


@app.route('/api/movies', methods = ['GET'])
def movies():
    return get_all_movies()


@app.route('/api/actor', methods = ['GET','POST','PUT','DELETE'])
def actor():
    if request.method == 'GET':
        get_actor_by_id()
    elif request.method == 'POST':
        add_actor()
    elif request.method == 'PUT':
        update_actor()
    elif request.method == 'DELETE':
        delete_actor()


@app.route('/api/movie', methods = ['GET','POST','PUT','DELETE'])
def movie():
    if request.method == 'GET':
        get_movie_by_id()
    elif request.method == 'POST':
        add_movie()
    elif request.method == 'PUT':
        update_movie()
    elif request.method == 'DELETE':
        delete_movie()


@app.route('/api/actor-relations', methods = ['PUT','DELETE'])
def actor_relations():
    if request.method == 'PUT':
        actor_add_relation()
    elif request.method == 'DELETE':
        actor_clear_relations()


@app.route('/api/movie-relations', methods = ['PUT','DELETE'])
def movie_relations():
    if request.method == 'PUT':
        movie_add_relation()
    elif request.method == 'DELETE':
        movie_clear_relations()
