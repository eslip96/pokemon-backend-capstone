from flask import Blueprint, request, jsonify

import controllers

auth = Blueprint('auth', __name__)


@auth.route('/user/auth', methods=['POST'])
def auth_token_add():
    return controllers.auth_token_add(request)


@auth.route('/user/logout/<auth_token>', methods=['PUT'])
def auth_token_remove(auth_token):
    return controllers.auth_token_remove(request, auth_token)
