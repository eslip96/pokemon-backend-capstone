from flask import jsonify, request
from db import db
from lib.authenicate import *
from models import *
from util.reflection import populate_object


@auth_admin
def add_type(req):
    post_data = req.form if req.form else req.json
    new_type = Type.new_type_obj()
    populate_object(new_type, post_data)
    try:
        db.session.add(new_type)
        db.session.commit()
        return jsonify({"message": "type created", "result": type_schema.dump(new_type)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to create type", "error": str(e)}), 400


@auth
def get_all_types(req):
    try:
        all_types = Type.query.all()
        return jsonify({"types": types_schema.dump(all_types)}), 200
    except Exception as e:
        return jsonify({"message": "unable to fetch types", "error": str(e)}), 400


@auth
def get_type_by_id(req, type_id):
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "type not found"}), 404
        return jsonify({"message": "type requested", "result": type_schema.dump(type)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "failed to retrieve type", "error": str(e)}), 400


@auth_admin
def update_type(req, type_id):
    post_data: req.form if req.form else req.json
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "type not found"}), 404

        populate_object(type, post_data)
        db.session.commit()

        return jsonify({"message": "type updated successfully", "type": type_schema.dump(type)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "failed to update type", "error": str(e)}), 400


@auth_admin
def delete_type(req, type_id):
    try:
        type = Type.query.get(type_id)
        if not type:
            return jsonify({"message": "type not found"}), 404

        db.session.delete(type)
        db.session.commit()

        return jsonify({"message": "type deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "failed to delete type", "error": str(e)}), 400
