from datetime import datetime
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from .models import User, Group, Responsibility
from . import db
from typing import List, Dict

# we are gonna want to make some design patterns for the chores here
# this means we want to do some oop?
# questions that need to be answered:
# 1. what types of chores to we have
# 2. what kinda design patterns can we  use to represent chores

chore = Blueprint('chore', __name__)

# Create Chore
@chore.route('/chore', methods=['POST'])
@login_required
def create_chore() -> Dict:
    name = request.form.get('name')
    description = request.form.get('description', default="")
    deadline = request.form.get('deadline')
    assignee = request.form.get('assignee', default=None)
    group_id = current_user.group_id
    
    new_chore = Responsibility(
        name = name,
        description = description, 
        deadline = deadline,
        assignee = assignee,
        group_id = group_id,
    )
    
    db.session.add(new_chore)
    db.session.commit()
    
    return (jsonify(new_chore.to_dict()), 201)
    
# View Chores
@chore.route('/my_chores', methods=['GET'])
@login_required
def view_my_chores() -> Dict:
    chores = Responsibility.query.filter_by(assignee=current_user.id).all()

    return (jsonify([c.to_dict() for c in chores.all()]), 200)

@chore.route('/group_chores', methods=['GET'])
@login_required
def view_group_chores() -> Dict:
    chores = Responsibility.query.filter_by(group_id=current_user.group_id).all()
    return (jsonify([c.to_dict() for c in chores.all()]), 200)

# Update Chore / mark chore as complete
@chore.route('/chore', methods=['PATCH'])
@login_required
def update_chore() -> Dict:
    id = request.form.get('id')
    name = request.form.get('name')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    assignee = request.form.get('assignee')
    completed = request.form.get('completed', default=False)

    chore = Responsibility.query.filter_by(id=id)
    
    if name:
        chore.name = name
    if description:
        chore.description = description
    if deadline:
        chore.deadline = deadline # not sure if this is datetime object might have to cast it
    if assignee:
        chore.assignee = int(assignee)
    if completed:
        chore.completed_at = datetime.now()
    
    db.session.commit()
    
    return (jsonify(chore.to_dict()), 200)

# Delete Chore
@chore.route('/chore', methods=['DELETE'])
@login_required
def delete_chore() -> Dict:
    id = request.form.get('id')
    
    chore = Responsibility.query.filter_by(id=id)
    chore.completed_at = datetime.now()
    
    db.session.commit()
    
    return (jsonify(chore.to_dict()), 200)