from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


@auth_admin
def add_pokemon(req):
    post_data = req.form if req.form else req.json
    new_pokemon = Pokemon.new_pokemon_obj()
    populate_object(new_pokemon, post_data)
    try:
        db.session.add(new_pokemon)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "unable to create Pokemon"}), 400

    return jsonify({"message": "pokemon created", "result": pokemon_schema.dump(new_pokemon)}), 201


@auth
def get_all_pokemon(req):
    try:
        all_pokemon = Pokemon.query.all()
        return jsonify({"pokemon": pokemons_schema.dump(all_pokemon)}), 200
    except:
        return jsonify({"message": "unable to fetch Pokemon"}), 400


@auth_admin
def update_pokemon(req, pokemon_id):
    try:
        pokemon = Pokemon.query.get(pokemon_id)
        if not pokemon:
            return jsonify({"message": "pokemon not found"}), 404

        data = req.form if req.form else req.json

        if 'pokemon_name' in data:
            pokemon.pokemon_name = data['pokemon_name']
        if 'type_id' in data:
            pokemon.type_id = data['type_id']
        if 'description' in data:
            pokemon.description = data['description']

        db.session.commit()

        return jsonify({"message": "pokemon updated successfully", "pokemon": pokemon_schema.dump(pokemon)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update Pokemon"}), 400


@auth
def get_pokemon_by_id(req, pokemon_id):
    try:
        pokemon = Pokemon.query.filter_by(pokemon_id).first()
        if not pokemon:
            return jsonify({"message": "no pokemon in the database with the provided id"}), 404
        return jsonify({"message": "pokemon requested", "result": pokemon_schema.dump(pokemon)}), 200
    except:
        return jsonify({"message": "failed to retrieve pokemon"}), 400


@auth_admin
def delete_pokemon(req, pokemon_id):
    try:

        pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()

        if not pokemon:
            return jsonify({"message": "no pokemon found with the given id"}), 404

        deleted_pokemon = pokemon_schema.dump(pokemon)

        db.session.delete(pokemon)
        db.session.commit()

        return jsonify({"message": "pokemon and any associated data have been deleted", "deleted pokemon": deleted_pokemon}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "failed to delete pokemon"}), 400
