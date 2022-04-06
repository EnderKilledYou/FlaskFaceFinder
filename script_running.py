from flask import Blueprint, abort, Response
from flask_login import login_required, current_user

from app import db
from helpers import return_as_json
from orm import UserImage
from script_running_helper import image_neural_enhance

script_running = Blueprint('script_running', __name__)


# /Neural enhance options ####################
@script_running.route('/neural_enhance/<id>/', methods=['GET'])
@login_required
def neural_enhance(id):
    user_image = UserImage.query.filter_by(id=id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    root_id = user_image.root_id
    if user_image.root_id == 0:
        root_id = user_image.id
    image_data = image_neural_enhance(user_image)

    new_image = UserImage(parent_id=user_image.parent_id, user_id=current_user.id, data=image_data,
                          root_id=root_id)
    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())


