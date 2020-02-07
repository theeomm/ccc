from flask import request, jsonify
from flask.views import MethodView

from app import datastore, db
from .schema import User, UserSchema


class UserAPI(MethodView):
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()

        if 'email' not in data:
            return jsonify({
                'error': 'Email address is required'
            }), 400

        if 'password' not in data:
            return jsonify({
                'error': 'Password is required'
            }), 400

        user = datastore.create_user(
            email=data['email'],
            password=data['password'],
        )

        print(f"############## {user} ############")

        db.session.commit()

        return jsonify({'message': 'user created'}), 201

    def get(self, id):
        """
        Retrieve users
        """
        # data = request.get_json()

        if id is None:
            users = User.query.all()

            return UserSchema(many=True).dump(users)

        user = User.query.get(id)

        if user is None:
            return jsonify(self.error['Invalid user ID']), 404

        return UserSchema().dump(user)
