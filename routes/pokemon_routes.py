from flask import Blueprint, request, jsonify

import controllers

pokemon = Blueprint('pokemon', __name__)


@pokemon.route('/pokemon', methods=['POST'])
def add_pokemon():
    return controllers.add_pokemon(request)


@pokemon.route('/pokemons', methods=['GET'])
def get_all_pokemon():
    return controllers.get_all_pokemon(request)


@pokemon.route('/pokemon/<pokemon_id>', methods=['PUT'])
def update_pokemon(pokemon_id):
    return controllers.update_pokemon(request, pokemon_id)


@pokemon.route('/pokemon/ability/<pokemon_id>', methods=['PUT'])
def add_ability_to_pokemon(pokemon_id):
    return controllers.add_ability_to_pokemon(request, pokemon_id)


@pokemon.route('/pokemon/<pokemon_id>', methods=['GET'])
def get_pokemon_by_id(pokemon_id):
    return controllers.get_pokemon_by_id(request, pokemon_id)


@pokemon.route('/pokemon/delete/<pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    return controllers.delete_pokemon(request, pokemon_id)
