from flask import Blueprint, request, jsonify

import controllers

pokemon = Blueprint('pokemon', __name__)


@pokemon.route('/pokemon', methods=['POST'])
def add_pokemon():
    return controllers.add_pokemon(request)
