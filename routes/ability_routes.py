from flask import Blueprint, request, jsonify

import controllers

ability = Blueprint('ability', __name__)


@ability.route('/ability', methods=['POST'])
def add_ability():
    return controllers.add_ability(request)


@ability.route('/abilities', methods=['GET'])
def get_all_abilities():
    return controllers.get_all_abilities(request)


@ability.route('/ability/<ability_id>', methods=['GET'])
def get_ability_by_id(ability_id):
    return controllers.get_ability_by_id(request, ability_id)


@ability.route('/ability/<ability_id>', methods=['PUT'])
def update_ability(ability_id):
    return controllers.update_ability(request, ability_id)


@ability.route('/ability/delete/<ability_id>', methods=['DELETE'])
def delete_ability(ability_id):
    return controllers.delete_ability(request, ability_id)
