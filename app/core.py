
from tokenize import Token
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from .models import User, Group, Responsibility, Token as DBToken
from . import db
from typing import List, Dict
from pyfcm import FCMNotification
from dotenv import load_dotenv
import os

load_dotenv()
FCM_KEY = os.getenv('FCM_KEY')

core = Blueprint('core', __name__)
app = Flask(__name__)

# just a base placeholder to see if the app is online
@core.route("/", methods=['GET'])
def home():
  return "CS446!!!"

# returns current user
# @core.route("/whoami", methods=['GET'])
#@login_required
# def whoami() -> Dict:
#   return (jsonify(current_user.to_dict()), 200)


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
#@login_required
def create_group() -> Dict:
  id = request.form.get("id")
  name = request.form.get('name')
  description = request.form.get('description', default="")
  
  user = User.query.filter_by(id=id).first()

  # we should enforce that a user can only be in 1 group at a time
  if user.group_id:
    return (jsonify({"ERROR":"USER ALREADY IN GROUP"}), 400)
  
  # group names should be unique ?
  if Group.query.filter_by(name=name).first():
    return (jsonify({"ERROR":"GROUP NAME ALREADY TAKEN"}), 400)
  
  # create a new group with the form data.
  new_group = Group(name=name, description=description)
    
  db.session.add(new_group)
  db.session.flush()
  
  # set each user's group_id to the new group
  user.group_id = new_group.id

  db.session.commit()
  
  return (jsonify(new_group.to_dict()), 201)


# Get the user's current group
@core.route('/group', methods=['GET'])
#@login_required
def get_group() -> Dict:
  id = request.args.get("id")
  user = User.query.filter_by(id=id).first()
  group = user.group
  group = group.to_dict() if group else {}
  
  return (jsonify(group), 200)


# Leave a group, if a group is empty, delete it and it's chores
# TODO: when leave a group, set all assigned chores to unassigned
# TODO: when leave a group as last person, delete all chores for that group
@core.route('/leave_group', methods=['DELETE'])
#@login_required
def leave_group() -> Dict:
  id = request.form.get("id")
  user = User.query.filter_by(id=id).first()
  
  # make sure user is in a group
  if user.group_id == 0:
    return (jsonify({"ERROR": "USER IS NOT IN GROUP"}), 400)
  
  group = user.group
  
  # leave the group
  user.group_id = None
  
  # if the group has no users we can delete the group
  if not User.query.filter_by(group_id=group.id).all():
    db.session.delete(group)
  
  db.session.commit()
  
  return (jsonify(user.to_dict()), 200)


@core.route('/join_group', methods=['POST'])
#@login_required
def join_group() -> Dict:
  id = request.form.get("id")
  group_id = request.form.get("group_id")
  group = Group.query.filter_by(id=int(group_id)).first()
  
  # make sure group exists
  if not group:
    return (jsonify({"ERROR": "GROUP DOES NOT EXIST"}), 400)
  
  # join the group
  user = User.query.filter_by(id=id).first()
  user.group_id = int(group_id)
  
  db.session.commit()
  
  return (jsonify(user.to_dict()), 200)


@core.route('/badges', methods=['GET'])
#@login_required
def get_badges() -> Dict:
  pass


################
# NOTIFICATIONS
################

def send_fcm(fcm_tokens, title=None, body=None):
    push_service = FCMNotification(api_key=FCM_KEY)
    try:
        if type(fcm_tokens) is list:
            result = push_service.notify_multiple_devices(registration_ids=fcm_tokens, message_title=title, message_body=body)
            return result
        else:
            result = push_service.notify_single_device(registration_id=fcm_tokens, message_title=title, message_body=body)
            return result
    except Exception as e:
        return e

@core.route('/send_message', methods=['POST'])
#@login_required
def send_message() -> Dict:
  target_id = request.form.get("target_id")
  tokens = DBToken.query.filter_by(user_id=int(target_id)).all()
  tokens = [t.token for t in tokens]
  title = target_id = request.form.get("title")
  body = request.form.get("body")

  res = send_fcm(tokens, title, body)

  print(res)

  return res

@core.route('/token', methods=['POST'])
#@login_required
def send_token() -> Dict:
  user_id = request.form.get('user_id')
  token = request.form.get('token')
  
  existing_token = DBToken.query.filter_by(token=token).first()

  if existing_token:
    existing_token.user_id = user_id
    db.session.commit()
    return (jsonify(existing_token.to_dict()), 200)

  else:
    new_token = DBToken(user_id=user_id, token=token)
    db.session.add(new_token)
    db.session.flush()
    db.session.commit()
    return (jsonify(new_token.to_dict()), 200)

  
