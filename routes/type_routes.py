from flask import Blueprint, request, jsonify

import controllers

type = Blueprint('type', __name__)


@type.route('/type', methods=['POST'])
def add_type():
    return controllers.add_type(request)


@type.route('/types', methods=['GET'])
def get_all_types():
    return get_all_types()


@type.route('/type/<type_id>', methods=['GET'])
def get_type_by_id(type_id):
    return controllers.get_type_by_id(type_id, request)


@type.route('/type/<type_id>', methods=['PUT'])
def update_type(type_id):
    return controllers.update_type(type_id, request)


@type.route('/type/delete/<type_id>', methods=['DELETE'])
def delete_type(type_id):
    return controllers.delete_type(type_id)
