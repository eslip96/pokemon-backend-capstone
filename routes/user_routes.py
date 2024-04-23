from flask import Blueprint, request, jsonify

import controllers
# from controllers.user_controller import add_user


users = Blueprint('users', __name__)


@users.route('/pokemon/user', methods=['POST'])
def add_NEW_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def get_all_users():
    return controllers.get_all_users(request)


@users.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return controllers.delete_user(request, user_id)
