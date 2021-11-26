from flask_restx import Resource, Namespace
from flask import request

from models import User
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        req_json = request.json
        user = User(**req_json)
        db.session.add(user)
        db.session.commit()
        return "", 201, {"location": f"/movies/{user.id}"}