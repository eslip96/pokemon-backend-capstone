from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


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
        db.session.rollback()
        return jsonify({"message": "unable to create team", "error": str(e)}), 400


@auth
def get_all_teams(req):
    try:
        all_teams = Team.query.all()
        return jsonify({"teams": teams_schema.dump(all_teams)}), 200
    except Exception as e:
        return jsonify({"message": "unable to fetch teams", "error": str(e)}), 400


@auth
def get_team_by_id(team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "team not found"}), 404
        return jsonify({"message": "requested team", "result": team_schema.dump(team)}), 200
    except Exception as e:
        return jsonify({"message": "failed to retrieve team", "error": str(e)}), 400


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
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to update team", "error": str(e)}), 400


@auth_admin
def delete_team(req, team_id):
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"message": "team not found"}), 404
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "team deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "failed to delete team", "error": str(e)}), 400
