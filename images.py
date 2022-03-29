import base64

from flask import Blueprint, request, abort, Response
from flask_login import login_required, current_user

from app import db
from helpers import return_as_json, return_as_json_list
from images_schema import image_upload_schema, get_image_schema
from orm import UserImage
from flask_expects_json import expects_json

images = Blueprint('images', __name__)


@images.route('/upload_image', methods=['POST'])
@login_required
@expects_json(image_upload_schema)
def upload_image():
    new_image = UserImage(parent_id=0, user_id=current_user.id, data=request.json['image'], root_id=0)
    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())


@images.route('/get_image', methods=['POST'])
@login_required
@expects_json(get_image_schema)
def get_image():
    user_image = UserImage.query.filter_by(id=request.json['image_id'], user_id=current_user.id).first()
    if user_image is None:
        abort(400,Response("No such image"))
    return return_as_json(user_image.to_dict())


@images.route('/get_images', methods=['GET'])
@login_required
def get_images():
    user_images = UserImage.query.filter_by(user_id=current_user.id).all()
    return return_as_json_list(user_images)
