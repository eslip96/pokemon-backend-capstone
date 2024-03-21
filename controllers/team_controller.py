from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


def add_team(req):
    post_data = req.form if req.form else req.json
    new_team = Team.new_team_obj()
    populate_object(new_team, post_data)
    try:
        db.session.add(new_team)
        db.session.commit()
        return jsonify({"message": "Team created", "result": team_schema.dump(new_team)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to create team", "error": str(e)}), 400


def get_all_teams():
    try:
        all_teams = Team.query.all()
        return jsonify({"teams": teams_schema.dump(all_teams)}), 200
    except Exception as e:
        return jsonify({"message": "Unable to fetch teams", "error": str(e)}), 400


def get_team_by_id(team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "Team not found"}), 404
        return jsonify({"team": team_schema.dump(team)}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve team", "error": str(e)}), 400


def update_team(team_id, req):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "Team not found"}), 404

        data = req.form if req.form else req.json
        populate_object(team, data)

        db.session.commit()

        return jsonify({"message": "Team updated successfully", "team": team_schema.dump(team)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to update team", "error": str(e)}), 400


def delete_team(team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "Team not found"}), 404
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "Team deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete team", "error": str(e)}), 400
