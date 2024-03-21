from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


def add_pokemon(req):
    post_data = req.form if req.form else req.json
    new_pokemon = Pokemon.new_pokemon_obj()
    populate_object(new_pokemon, post_data)
    try:
        db.session.add(new_pokemon)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Unable to create Pokemon"}), 400

    return jsonify({"message": "Pokemon created", "result": pokemon_schema.dump(new_pokemon)}), 201


def get_all_pokemon():
    try:
        all_pokemon = Pokemon.query.all()
        return jsonify({"pokemon": pokemons_schema.dump(all_pokemon)}), 200
    except Exception as e:
        return jsonify({"message": "Unable to fetch Pokémon", "error": str(e)}), 400


def update_pokemon(pokemon_id, req):
    try:
        pokemon = Pokemon.query.get(pokemon_id)
        if not pokemon:
            return jsonify({"message": "Pokemon not found"}), 404

        data = req.form if req.form else req.json

        if 'name' in data:
            pokemon.name = data['name']
        if 'type_id' in data:
            pokemon.type_id = data['type_id']
        if 'ability_id' in data:
            pokemon.ability_id = data['ability_id']
        if 'description' in data:
            pokemon.description = data['description']
        if 'base_stats' in data:
            pokemon.base_stats = data['base_stats']

        db.session.commit()

        return jsonify({"message": "Pokemon updated successfully", "pokemon": pokemon_schema.dump(pokemon)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to update Pokemon", "error": str(e)}), 400


def get_pokemon_by_id(pokemon_id):
    try:
        pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
        if not pokemon:
            return jsonify({"message": "No Pokémon in the database with the provided ID"}), 404
        return jsonify({"message": "Pokémon requested", "result": pokemon_schema.dump(pokemon)}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve Pokémon", "error": str(e)}), 400


def delete_pokemon(pokemon_id):
    try:

        pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()

        if not pokemon:
            return jsonify({"message": "No Pokémon found with the given ID"}), 404

        deleted_pokemon = pokemon_schema.dump(pokemon)

        db.session.delete(pokemon)
        db.session.commit()

        return jsonify({"message": "Pokémon and any associated data have been deleted", "deleted_pokemon": deleted_pokemon}), 200
    except Exception as e:

        print(e)
        db.session.rollback()
        return jsonify({"message": "Failed to delete Pokémon", "error": str(e)}), 400
