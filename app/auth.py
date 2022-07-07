from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return (jsonify({"ERROR": "INVALID LOGIN DETAILS"}), 404)
    
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=False)
    return (jsonify(user.as_dict()), 200)

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return (jsonify(user.as_dict()), 200)

    # create a new user with the form data. Hash the password
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    
    return (jsonify(new_user.as_dict()), 201)

@auth.route('/logout')
@login_required
def logout():
    name = current_user.name
    logout_user()
    return f'{name} logged out'