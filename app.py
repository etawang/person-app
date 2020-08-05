import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///person.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from person_service import PersonService

ps = PersonService()


@app.route("/persons", methods=["GET"])
def list_all_persons():
    return jsonify(ps.read_all())


@app.route("/persons", methods=["POST"])
def create_person():
    person_data = request.get_json()
    if not set(["first_name", "last_name", "email", "age"]) <= set(person_data.keys()):
        return "missing_required_fields", 400

    return ps.create(person_data), 201


@app.route("/persons/<person_id>", methods=["GET"])
def read_person(person_id):
    return ps.read(person_id)


@app.route("/persons/<person_id>/<version>", methods=["GET"])
def read_person_version(person_id, version):
    return ps.read_version(person_id, version)


@app.route("/persons/<person_id>", methods=["PUT"])
def put_person(person_id):
    person_data = request.get_json()
    if not set(["first_name", "last_name", "email", "age"]) <= set(person_data.keys()):
        return "missing_required_fields", 400

    ps.overwrite(person_id, person_data)
    return "", 204


@app.route("/persons/<person_id>", methods=["PATCH"])
def patch_person(person_id):
    ps.update(person_id, request.get_json())
    return "", 204


@app.route("/persons/<person_id>", methods=["DELETE"])
def delete_person(person_id):
    ps.delete(person_id)
    return "", 204
