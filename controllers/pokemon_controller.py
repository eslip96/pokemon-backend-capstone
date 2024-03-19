from flask import jsonify, request
from db import db
from lib.authenicate import *


@app.route('/pokemon/add', methods=['POST'])
def add_pokemon():
    try:
        data = request.json

        new_pokemon = Pokemon(
            name=data['name'],
            type_id=data['type_id'],
            ability_id=data['ability_id'],
            description=data['description'],
            base_stats=data['base_stats']
        )

        db.session.add(new_pokemon)

        db.session.commit()

        return jsonify({'message': 'Pokemon added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
