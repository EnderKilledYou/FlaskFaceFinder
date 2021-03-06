import base64
import io
import logging

from flask import Blueprint, request, abort, Response, send_file
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


@images.route('/get_image/<image_id>', methods=['GET'])
@login_required
def get_image(image_id):
    user_image = UserImage.query.filter_by(id=image_id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    return return_as_json(user_image.to_dict())


@images.route('/delete_image/<image_id>', methods=['GET'])
@login_required
def delete_image(image_id):
    user_image: UserImage = UserImage.query.filter_by(id=image_id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    db.session.delete(user_image);
    db.session.commit()
    db.session.flush()
    return return_as_json({})


@images.route('/get_image_view/<id>', methods=['GET'])
def get_image_view(id):
    # , user_id=current_user.id
    user_image = UserImage.query.filter_by(id=id).first()
    if user_image is None:
        abort(400, Response("No such image"))

    img_bytes = base64.b64decode(user_image.data)
    img = io.BytesIO()
    img.write(img_bytes)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@images.route('/get_images', methods=['GET'])
@login_required
def get_images():
    user_images = UserImage.query.filter_by(user_id=current_user.id).all()
    return return_as_json_list(user_images)

@images.route('/get_images/<root_id>', methods=['GET'])
@login_required
def get_root_images(root_id):
    user_images = UserImage.query.filter_by(user_id=current_user.id,root_id=root_id).all()
    return return_as_json_list(user_images)


@images.route('/get_images_by_parent/<parent_id>', methods=['GET'])
@login_required
def get_images_by_parent(parent_id):
    user_images = UserImage.query.filter_by(user_id=current_user.id,parent_id=parent_id).all()
    return return_as_json_list(user_images)