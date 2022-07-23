from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Group
from . import db
from typing import List, Dict


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST"])
def login() -> Dict:
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return (jsonify({"ERROR": "INVALID LOGIN DETAILS"}), 404)
    
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    return (jsonify(user.to_dict()), 200)


@auth.route('/logout')
#@login_required
def logout() -> str:
    name = ""
    if request.args.get("name"):
        return f'{name} logged out'
    
    return f'{name} logged out'
    


@auth.route('/signup', methods=['POST'])
def signup_post() -> Dict:
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    about = request.form.get('about')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return (jsonify(user.to_dict()), 200)

    # create a new user with the form data. Hash the password
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256'),
        about=about
    )

    db.session.add(new_user)
    db.session.commit()
    
    return (jsonify(new_user.to_dict()), 201)


@auth.route('/users', methods=['GET'])
#@login_required
def get_users() -> List[Dict]:
    args = request.args
    users = User.query
    
    # if we search by id we return a single user
    if args.get("id", default=0, type=int):
        users = User.query.filter_by(id=args.get("id", default=0, type=int))
        print(args.get("id", default=0, type=int))
        print(str(users))
        return (jsonify([users.first().to_dict()]), 200)
    
    # query by group
    if args.get("group_id", default=-1, type=int):
        group_id = args.get("group_id", default=-1, type=int)
        
        if group_id == -1:
            users = users.filter(Group.group_id.is_(None))
        else:
            users = users.filter_by(group_id=group_id)
        
    
    # query by name
    if args.get("name", default=""):
        users = users.filter_by(name=args.get("name"), default="")
    

    return (jsonify([u.to_dict() for u in users.all()]), 200)




@auth.route('/user', methods=['PATCH'])
#@login_required
def update_user() -> Dict:
    id = int(request.form.get("id"))
    user = User.query.filter_by(id=id).first()
    
    name = request.form.get('name')
    password = request.form.get('password')
    about = request.form.get('about', default="")
    avatar = request.form.get('avatar', default=0, type=int)
    
    if name:
        user.name = name
    if password:
        user.password = generate_password_hash(password, method='sha256')
    if about:
        user.about = about
    if avatar:
        user.avatar = avatar
    
    db.session.commit()
    
    return (jsonify(user.to_dict()), 200)
    

# logs out and deletes the current user
@auth.route('/user', methods=['DELETE'])
#@login_required
def delete_user() -> Dict:
    id = int(request.form.get("id"))
    user = User.query.filter_by(id=id).first()
    ret = jsonify(user.to_dict())
    logout_user()
    
    db.session.delete(user)
    db.session.commit()
    
    
    return (ret, 200)
    