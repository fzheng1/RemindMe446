from email.policy import default
from enum import unique
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    about = db.Column(db.String(2000))
    mmr = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    responsibilities = db.relationship('Responsibility', backref='user')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Group(db.Model):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(2000))
    users = db.relationship('User', backref='group')
    responsibilities = db.relationship('Responsibility', backref='group')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    

class Responsibility(db.Model):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    value = db.Column(db.Integer) # Should be rated 1-10
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    is_done = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
