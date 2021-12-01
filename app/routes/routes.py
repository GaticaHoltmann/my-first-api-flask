from os import access
from flask import Blueprint, json, request, jsonify
from database import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.models import User, Movie
from schemas.schemas import movies_schema, movie_schema
import bcrypt

blue_print = Blueprint('app', __name__)


# init
@blue_print.route('/', methods=['GET'])
def inicio():
    # return jsonify(response='Rest API with Python, Flask and Mysql')
    return "<h1> hola amor </h1>"


# register user
@blue_print.route('/auth/register', methods=['POST'])
def register_user():
    try:
        print(request.json)
        user = request.json.get('user')
        password = request.json.get('password')
        if not user or not password:
            return jsonify(response='invalids fields'), 400

        exists_user = User.query.filter_by(user=user).first()
        if exists_user:
            return jsonify(response='User already exists'), 400

        password_encrypt = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(user, password_encrypt)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(response="User created"), 201

    except Exception:
        return jsonify(response='Error en request'), 500


@blue_print.route('/auth/login', methods=['POST'])
def init_session():
    try:
        user = request.json.get('user')
        password = request.json.get('password')
        if not user or not password:
            return jsonify(response='invalids fields'), 400

        exists_user = User.query.filter_by(user=user).first()
        if not exists_user:
            return jsonify(response='User not exists'), 404

        is_valid_password = bcrypt.checkpw(password.encode(
            'utf-8'), exists_user.password.encode('utf-8'))
        if is_valid_password:
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token),200
        return jsonify(response='user or password incorrect'), 404

    except Exception:
        return jsonify(response='Error en request'), 500

# protected routes

@blue_print.route('/api/movies', methods=['POST'])
@jwt_required()
def create_movie():
    try:
        name = request.json['name']
        year = request.json['year']
        director = request.json['director']
        repart = request.json['repart']
        genre = request.json['genre']
        trailer = request.json['trailer']

        new_movie = Movie(name,year,director,repart,genre,trailer)

        db.session.add(new_movie)
        db.session.commit()

        return jsonify(response='movie added successuflly'), 201
    except Exception:
        return jsonify(response='Error en request'), 500


@blue_print.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    try:
        movies = Movie.query.all()
        response= movies_schema.dump(movies)

        return movies_schema.jsonify(response),200
    except Exception:
        return jsonify(response='Error en request'), 500


@blue_print.route('/api/movies/<int:id>', methods=['GET'])
@jwt_required()
def get_movie_by_id(id):
    try:

        movie = Movie.query.get(id)
        response= movie_schema.dump(movie)

        return movie_schema.jsonify(response),200
    except Exception:
        return jsonify(response='Error en request'), 500


@blue_print.route('/api/movies/<int:id>', methods=['PUT'])
@jwt_required()
def update_movie(id):
    try:
        movie = Movie.query.get(id)
        if not movie:
            return jsonify(response='movie dont exists')
        

        movie.name = request.json['name']
        movie.year = request.json['year']
        movie.director = request.json['director']
        movie.repart = request.json['repart']
        movie.genre = request.json['genre']
        movie.trailer = request.json['trailer']
        
        db.session.commit()

        return jsonify(response='movie updated successuflly'), 201
    except Exception:
        return jsonify(response='Error en request'), 500

@blue_print.route('/api/movies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movie_by_id(id):
    try:

        movie = Movie.query.get(id)
        if not movie:
            return jsonify(response='Movie dont exists'),404
        db.session.delete(movie)
        db.session.commit()
        return jsonify(response='movie deleted successufully'),200
    except Exception:
        return jsonify(response='Error en request'), 500