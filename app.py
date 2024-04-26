import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from db import *
from util.blueprints import register_blueprints


app = Flask(__name__)

app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')


database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")


app.config["SQLALCHEMY_DATABASE_URI"] = f'{database_scheme}://{database_address}:{database_port}/{database_name}'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)
CORS(app)


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created succesfully")


register_blueprints(app)

if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port, debug=True)
