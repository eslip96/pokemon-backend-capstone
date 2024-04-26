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
            return jsonify({"message": "no users found"}), 404

        num_user = users_schema.dump(all_users)
        return jsonify({"message": "success", "results": num_user}), 200
    except:
        return jsonify({"message": "unable to pull users"}), 400


@auth_admin
def update_user(req, user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "user not found"}), 404

        data = req.form if req.form else req.json

        if 'password' in data:
            data['password'] = generate_password_hash(data['password']).decode('utf8')

        populate_object(user, data)
        db.session.commit()

        return jsonify({"message": "user updated successfully", "user": user_schema.dump(user)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": f"unable to update user"}), 400


@auth_admin
def get_user_by_id(request, user_id):
    try:
        user = Users.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "user not found"}), 404
        return jsonify({"message": "user requested", "result": user_schema.dump(user)}), 200
    except:
        db.session.rollback()
        return ({"message": "failed to retrieve user"}), 400


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
