from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object
from flask_bcrypt import generate_password_hash
from models.users import Users, user_schema, users_schema


def add_user(req):
    post_data = req.json
    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    if 'password' not in post_data or not isinstance(post_data['password'], str):
        return jsonify({'message': 'password is required thats not numbers and must be in qoutes'}), 400

    new_user.password = generate_password_hash(post_data['password']).decode('utf8')
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create user'}), 400
    return jsonify({'message': 'user created', 'result': user_schema.dump(new_user)}), 200


@auth_admin
def get_all_users(req):
    try:
        all_users = db.session.query(Users).all()

        if not all_users:
            return jsonify({"message": "No users found"}), 404

        num_user = users_schema.dump(all_users)
        return jsonify({"message": "Success", "results": num_user}), 200
    except Exception as e:
        return jsonify({"message": "Unable to pull users", "error": str(e)}), 400


@auth_admin
def delete_user(request, user_id):
    if not validate_token(request):
        return jsonify({'message': 'invalid token'}), 401

    try:
        user_to_delete = Users.query.get(user_id)

        if user_to_delete is None:
            return jsonify({'message': 'user not found'}), 404

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({'message': 'user deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to delete user'}), 400
