from flask_restx import Resource, Namespace
from flask import request
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return GenreSchema().dump(new_genre), 201

@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200


    def delete(self, id):
        genre = Genre.query.get(id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
        return '', 204

    def put(self, id: int):
        genre = Genre.query.get(id)
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204