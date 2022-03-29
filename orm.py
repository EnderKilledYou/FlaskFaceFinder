import json
from dataclasses import dataclass

from flask_sqlalchemy import Model

from app import db
from flask_login import UserMixin
from flask import Blueprint
from sqlalchemy_serializer import SerializerMixin

orm = Blueprint('orm', __name__)


class User(UserMixin, db.Model, SerializerMixin):
    serialize_rules = ()
    serialize_only = ('id', 'email', 'name')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class UserImage(db.Model, SerializerMixin):
    serialize_only = ('id', 'parent_id','root_id', 'user_id', 'data')
    serialize_rules = ()
    id = db.Column(db.Integer, primary_key=True,index=True)
    root_id = db.Column(db.Integer,index=True)
    parent_id = db.Column(db.Integer,index=True)
    user_id = db.Column(db.Integer,index=True)
    data = db.Column(db.Text)
