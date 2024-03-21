from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


def create_ability(req):
    post_data = req.form if req.form else req.json
    new_ability = Ability()
    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()
        return jsonify({"message": "Ability created", "result": ability_schema.dump(new_ability)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to create ability", "error": str(e)}), 400


def get_all_abilities(req):
    try:
        abilities = db.session.query(Ability).all()
        if not abilities:
            return jsonify({"message": "No abilities found"}), 404

        return jsonify({"message": "Current abilities in database", "results": abilities_schema.dump(abilities)}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve abilities", "error": str(e)}), 400


def get_ability_by_id(ability_id):
    try:
        ability = Ability.query.filter_by(ability_id=ability_id).first()
        if not ability:
            return jsonify({"message": "No ability in the database with the provided ID"}), 404
        return jsonify({"message": "Ability requested", "result": ability_schema.dump(ability)}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve ability", "error": str(e)}), 400


def update_ability(req, ability_id):
    post_data = req.form if req.form else req.json
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "Ability not found"}), 404
        populate_object(ability, post_data)
        db.session.commit()
        return jsonify({"message": "Ability updated successfully", "result": ability.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to update ability", "error": str(e)}), 400


def delete_ability(ability_id):
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "Ability not found"}), 404
        db.session.delete(ability)
        db.session.commit()
        return jsonify({"message": "Ability deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to delete ability", "error": str(e)}), 400
