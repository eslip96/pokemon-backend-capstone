from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object
from models.ability import Ability, abilities_schema, ability_schema
from models.pokemon import Pokemon, pokemon_schema, pokemons_schema


@auth_admin
def add_ability(req):
    post_data = req.form if req.form else req.json
    new_ability = Ability.new_ability_obj()
    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()
        return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create ability"}), 400


@auth
def get_all_abilities(req):
    try:
        abilities = db.session.query(Ability).all()
        if not abilities:
            return jsonify({"message": "no abilities found"}), 404

        return jsonify({"message": "current abilities in database", "results": abilities_schema.dump(abilities)}), 200
    except:
        return jsonify({"message": "failed to retrieve abilities"}), 400


@auth
def get_ability_by_id(req, ability_id):
    try:
        ability = Ability.query.filter_by(ability_id=ability_id).first()
        if not ability:
            return jsonify({"message": "ability not found"}), 404
        return jsonify({"message": "ability requested", "result": ability_schema.dump(ability)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "failed to retrieve ability"}), 400


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
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update ability"}), 400


@auth_admin
def delete_ability(req, ability_id):
    try:
        ability = Ability.query.get(ability_id)
        if not ability:
            return jsonify({"message": "ability not found"}), 404

        ability_pokemon = Pokemon.query.filter_by(ability_id=ability_id).all()

        for pokemon in ability_pokemon:
            pokemon.ability_id = None

        db.session.delete(ability)
        db.session.commit()
        return jsonify({"message": "ability deleted successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete ability"}), 400
