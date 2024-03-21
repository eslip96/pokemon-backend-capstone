from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


def create_type(req):
    post_data = req.form if req.form else req.json
    new_type = Type.new_type_obj()
    populate_object(new_type, post_data)
    try:
        db.session.add(new_type)
        db.session.commit()
        return jsonify({"message": "Type created", "result": type_schema.dump(new_type)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to create type", "error": str(e)}), 400


def get_all_types():
    try:
        all_types = Type.query.all()
        return jsonify({"types": types_schema.dump(all_types)}), 200
    except Exception as e:
        return jsonify({"message": "Unable to fetch types", "error": str(e)}), 400


def get_type_by_id(type_id, req):
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "Type not found"}), 404

        populate_object(type, req.form if req.form else req.json)
        db.session.commit()

        return jsonify({"type": type_schema.dump(type)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to retrieve type", "error": str(e)}), 400


def update_type(type_id, req):
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "Type not found"}), 404

        populate_object(type, req.form if req.form else req.json)
        db.session.commit()

        return jsonify({"message": "Type updated successfully", "type": type_schema.dump(type)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update type", "error": str(e)}), 400


def delete_type(type_id):
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "Type not found"}), 404

        db.session.delete(type)
        db.session.commit()

        return jsonify({"message": "Type deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete type", "error": str(e)}), 400
