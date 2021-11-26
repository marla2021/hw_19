from flask_restx import Resource, Namespace
from flask import request
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return DirectorSchema().dump(new_director), 201

@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def delete(self,id):
        director = Director.query.get(id)
        if director:
            db.session.delete(director)
            db.session.commit()
        return '', 204
    def put(self, id:int):
        director = Director.query.get(id)
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204