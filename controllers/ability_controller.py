from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


@auth_admin
def add_ability(req):
    post_data = req.form if req.form else req.json
    new_ability = Ability.new_ability_obj()
    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()
        return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to create ability", "error": str(e)}), 400


@auth
def get_all_abilities(req):
    try:
        abilities = db.session.query(Ability).all()
        if not abilities:
            return jsonify({"message": "no abilities found"}), 404

        return jsonify({"message": "current abilities in database", "results": abilities_schema.dump(abilities)}), 200
    except Exception as e:
        return jsonify({"message": "failed to retrieve abilities", "error": str(e)}), 400


@auth
def get_ability_by_id(req, ability_id):
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "ability not found"}), 404
        return jsonify({"message": "ability requested", "result": ability_schema.dump(ability)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "failed to retrieve ability", "error": str(e)}), 400


@auth_admin
def update_ability(req, ability_id):
    post_data = req.form if req.form else req.json
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "ability not found"}), 404
        populate_object(ability, post_data)
        db.session.commit()
        return jsonify({"message": "ability updated successfully", "result": ability_schema.dump(ability)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to update ability", "error": str(e)}), 400


@auth_admin
def delete_ability(req, ability_id):
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "ability not found"}), 404
        db.session.delete(ability)
        db.session.commit()
        return jsonify({"message": "ability deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to delete ability", "error": str(e)}), 400
