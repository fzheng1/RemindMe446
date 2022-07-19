
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from .models import User, Group, Responsibility
from . import db
from typing import List, Dict

core = Blueprint('core', __name__)

# just a base placeholder to see if the app is online
@core.route("/", methods=['GET'])
def home():
  return "CS446!!!"

# returns current user
@core.route("/whoami", methods=['GET'])
@login_required
def whoami() -> Dict:
  return (jsonify(current_user.to_dict()), 200)


####################
# PUBLIC FUNCTIONS
####################

# Get all groups
@core.route('/groups', methods=['GET'])
def get_groups() -> List[Dict]:
  groups = Group.query.all()
  return (jsonify([g.to_dict() for g in groups]), 200)


####################
# PRIVATE FUNCTIONS
####################

# Create a group for users not already in groups
@core.route('/group', methods=['POST'])
@login_required
def create_group() -> Dict:
  name = request.form.get('name')
  description = request.form.get('description', default="")

  # we should enforce that a user can only be in 1 group at a time
  if current_user.group_id:
    return (jsonify({"ERROR":"USER ALREADY IN GROUP"}), 400)
  
  # group names should be unique
  if Group.query.filter_by(name=name).first():
    return (jsonify({"ERROR":"GROUP NAME ALREADY TAKEN"}), 400)
  
  # create a new group with the form data.
  new_group = Group(name=name, description=description)
    
  db.session.add(new_group)
  db.session.flush()
  
  # set each user's group_id to the new group
  current_user.group_id = new_group.id

  db.session.commit()
  
  return (jsonify(new_group.to_dict()), 201)


# Get the user's current group
@core.route('/group', methods=['GET'])
@login_required
def get_group() -> Dict:
  group = current_user.group
  group = group.to_dict() if group else {}
  
  return (jsonify(group), 200)

# Leave a group, if a group is empty, delete it and it's chores
# TODO: when leave a group, set all assigned chores to unassigned
# TODO: when leave a group as last person, delete all chores for that group
@core.route('/leave_group', methods=['DELETE'])
@login_required
def leave_group() -> Dict:
  # make sure user is in a group
  if current_user.group_id == 0:
    return (jsonify({"ERROR": "USER IS NOT IN GROUP"}), 400)
  
  group = current_user.group
  
  # leave the group
  current_user.group_id = None
  
  # if the group has no users we can delete the group
  if not User.query.filter_by(group_id=group.id).all():
    db.session.delete(group)
  
  db.session.commit()
  
  return (jsonify(current_user.to_dict()), 200)


@core.route('/join_group', methods=['POST'])
@login_required
def join_group() -> Dict:
  group_id = request.form.get("group_id")
  group = Group.query.filter_by(id=int(group_id)).first()
  
  # make sure group exists
  if not group:
    return (jsonify({"ERROR": "GROUP DOES NOT EXIST"}), 400)
  
  # join the group
  current_user.group_id = int(group_id)
  
  db.session.commit()
  
  return (jsonify(current_user.to_dict()), 200)

