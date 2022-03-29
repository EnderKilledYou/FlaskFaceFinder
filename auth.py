from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, Response, jsonify
from flask_expects_json import expects_json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from auth_schemas import signup_schema, login_schema
from helpers import return_as_json
from orm import User
from app import db, app
import logging
logging.basicConfig(filename='auth.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@expects_json(login_schema)
def login_post():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return abort(401, Response("Nope."))

    login_user(user, remember=True)
    return return_as_json(user.to_dict())


@auth.route('/signup', methods=['POST'])
@expects_json(signup_schema)
def signup_post():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    try:
        user = User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database
    except Exception as e:
        app.logger.error(e)
        return abort(500, Response("Your request generated an internal error. Please contact the Admin and check "
                                   "auth.log"))

    if user:
        return abort(401, Response("Please sign in, user exists"))
    try:
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        db.session.flush()
    except Exception as e:
        app.logger.error(e)
        return abort(500, Response("Your request generated an internal error. Please contact the Admin and check "
                                   "auth.log"))

    return return_as_json(new_user.to_dict())


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return return_as_json({})
