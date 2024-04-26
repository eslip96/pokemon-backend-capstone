from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object
from models.team import Team, team_schema, teams_schema
from models.pokemon import Pokemon


@auth_admin
def add_team(req):
    post_data = req.form if req.form else req.json
    new_team = Team.new_team_obj()
    populate_object(new_team, post_data)
    try:
        db.session.add(new_team)
        db.session.commit()
        return jsonify({"message": "team created", "result": team_schema.dump(new_team)}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "unable to create team"}), 400


@auth
def get_all_teams(req):
    try:
        all_teams = Team.query.all()
        return jsonify({"teams": teams_schema.dump(all_teams)}), 200
    except:
        return jsonify({"message": "unable to fetch teams"}), 400


@auth
def get_team_by_id(req, team_id):
    try:
        team = Team.query.filter_by(team_id=team_id).first()
        if not team:
            return jsonify({"message": "team not found"}), 404
        return jsonify({"message": "requested team", "result": team_schema.dump(team)}), 200
    except:
        return jsonify({"message": "failed to retrieve team"}), 400


@auth_admin
def update_team(req, team_id):
    data = req.form if req.form else req.json
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "team not found"}), 404

        populate_object(team, data)

        db.session.commit()

        return jsonify({"message": "team updated successfully", "team": team_schema.dump(team)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update team"}), 400


def add_pokemon_to_team(req, team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "team not found"}), 404

        data = req.form if req.form else req.json
        pokemon_id = data.get('pokemon_id')

        if not pokemon_id:
            return jsonify({"message": "pokemon id is required"}), 400

        pokemon = Pokemon.query.get(pokemon_id)
        if not pokemon:
            return jsonify({"message": "pokemon not found"}), 404

        team.pokemons.append(pokemon)

        db.session.commit()

        return jsonify({"message": f"pokemon added to team successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": f"unable to add Pokemon to team"}), 400


@auth_admin
def delete_team(req, team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "team not found"}), 404
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "team deleted successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "failed to delete team"}), 400
