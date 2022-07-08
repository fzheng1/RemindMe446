from cmath import log
from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from . import db

core = Blueprint('core', __name__)

@core.route("/", methods=['GET'])
def home():
  return "index"

@core.route("/whoami", methods=['GET'])
@login_required
def whoami():
  return (jsonify(current_user.to_dict()), 200)


######
# GROUPS CRUD
######
# TODO


######
# GROUPS LOGIC
######
# TODO


######
# CHORE CRUD
######
# TODO


######
# CHORE LOGIC
######
# TODO