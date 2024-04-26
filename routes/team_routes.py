from flask import Blueprint, request, jsonify

import controllers

team = Blueprint('team', __name__)


@team.route('/team', methods=['POST'])
def add_teamn():
    return controllers.add_team(request)


@team.route('/teams', methods=['GET'])
def get_all_teams():
    return controllers.get_all_teams(request)


@team.route('/team/<team_id>', methods=['PUT'])
def update_team(team_id):
    return controllers.update_team(request, team_id)


@team.route('/team/<team_id>', methods=['GET'])
def get_team_by_id(team_id):
    return controllers.get_team_by_id(request, team_id)


@team.route('/team/pokemon/<team_id>', methods=['PUT'])
def add_pokemon_to_team(team_id):
    return controllers.add_pokemon_to_team(request, team_id)


@team.route('/team/delete/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    return controllers.delete_team(request, team_id)
