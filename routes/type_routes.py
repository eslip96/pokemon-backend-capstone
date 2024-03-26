from flask import Blueprint, request, jsonify

import controllers

type = Blueprint('type', __name__)
