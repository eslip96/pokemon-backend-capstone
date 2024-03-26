from flask import Blueprint, request, jsonify

import controllers

team = Blueprint('team', __name__)
