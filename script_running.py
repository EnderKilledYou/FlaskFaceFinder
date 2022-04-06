from flask import Blueprint, abort, Response
from flask_login import login_required, current_user

from app import db, app
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

    try:
        new_image = image_neural_enhance(user_image)

    except BaseException as fk:
        app.logger.error(fk)
        abort(500, Response('There was an error check the logs'))

    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())
