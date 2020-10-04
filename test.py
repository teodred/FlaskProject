from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from sqlalchemy import inspect
from flask import jsonify, make_response
from settings.constants import DB_URL,ACTOR_FIELDS,MOVIE_FIELDS
from core import db
from models.actor import Actor
from models.movie import Movie


data_actor = {'name': 'Megan Fox', 'gender': 'female', 'date_of_birth': dt.strptime('16.05.1986', '%d.%m.%Y').date()}
data_actor_upd = {'name': 'Not Megan Fox', 'gender': 'male', 'date_of_birth': dt.strptime('16.05.2000', '%d.%m.%Y').date()}

data_movie = {'name': 'Transformers', 'genre': 'action', 'year': 2007}
data_movie_upd = {'name': 'Teenage Mutant Ninja Turtles', 'genre': 'bad movie', 'year': 2014}

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db.init_app(app)

#with app.app_context():
#    db.create_all()
#    actor = Actor.create(**data_actor)
#    print('created actor:', actor.__dict__, '\\n')
#
#    movie = Movie.create(**data_movie)
#    print('created movie:', movie.__dict__, '\\n')

#    upd_actor = Actor.update(1, **data_actor_upd)
#    print('updated actor:', upd_actor.__dict__, '\\n')

#    upd_movie = Movie.update(1, **data_movie_upd)
#    print('updated movie:', upd_movie.__dict__, '\\n')

#    add_rels_actor = Actor.add_relation(1, upd_movie)
#    movie_2 = Movie.create(**data_movie)
#    add_more_rels_actor = Actor.add_relation(1, movie_2)
#    print('relations list:', add_more_rels_actor.filmography, '\\n')

#    clear_rels_actor = Actor.clear_relations(1)
#    print('all relations cleared:', clear_rels_actor.filmography, '\\n')

#    del_actor = Actor.delete(1)
#    print('actor deleted:', del_actor)
with app.app_context():
    db.create_all()
    def get_actor_by_id(data):
        """
        Get record by id
        """
        # data = get_request_data()
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)

            obj = Actor.query.filter_by(id=row_id).first()
            try:
                actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            return make_response(jsonify(actor), 200)

        else:
            err = 'No id specified'
            return make_response(jsonify(error=err), 400)

            obj = Actor.query.filter_by(id=row_id).first()
            try:
                actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)


    def add_actor(data):
        """
        Add new actor
        """
        #data = get_request_data()
        ### YOUR CODE HERE ###

        # use this for 200 response code
        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(new_actor), 200)
        ### END CODE HERE ###


    def get_all_actors():
        """
        Get list of all records
        """
        all_actors = Actor.query.all()
        actors = []
        for actor in all_actors:
            act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            actors.append(act)
            print(actors)
        return make_response(jsonify(actors), 200)


    def update_actor(data):
        """
        Update actor record by id
        """
        #data = get_request_data()
        ### YOUR CODE HERE ###

        # use this for 200 response code
        upd_record = Actor.update(1, **data)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)


    def delete_actor(data):
        """
        Delete actor by id
        """
        #data = get_request_data()
        ### YOUR CODE HERE ###
        Actor.delete(1)
        # use this for 200 response code
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
        ### END CODE HERE ###


    def actor_add_relation():
        """
        Add a movie to actor's filmography
        """
        #data = get_request_data()
        data = {'name': 'Megan Fox', 'gender': 'female', 'date_of_birth': dt.strptime('16.05.1986', '%d.%m.%Y').date(), 'name': 'Transformers', 'genre': 'action', 'year': 2007}
        ### YOUR CODE HERE ###
        movie_data = {k: v for k, v in data.items() if k in MOVIE_FIELDS}
        movie = Movie.create(movie_data)
        # use this for 200 response code
        actor = Actor.add_relation(data["id"], movie)  # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
        ### END CODE HERE ###

    add_actor(data_actor_upd)
    get_all_actors()
    update_actor(data_actor)
    get_all_actors()
    delete_actor(data_actor)
    get_all_actors()

