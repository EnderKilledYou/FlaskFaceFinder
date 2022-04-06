import base64
import io

import scipy
from flask import Blueprint, abort, Response
from flask_login import login_required, current_user

from app import db, app
from enhance import NeuralEnhancer
from helpers import return_as_json
from image_processing import create_image_from_array
from orm import UserImage

neural_enhance = Blueprint('neural_enhance', __name__)
enhancer = NeuralEnhancer(loader=False)


# /Neural enhance options ####################
@neural_enhance.route('/neural_enhance/<id>/', methods=['GET'])
@login_required
def neural_enhancer(id):
    user_image = UserImage.query.filter_by(id=id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    root_id = user_image.root_id
    if user_image.root_id == 0:
        root_id = user_image.id
    try:
        img_bytes = base64.b64decode(user_image.data)
        img_mem = io.BytesIO()
        img_mem.write(img_bytes)
        img_mem.seek(0)
        img = scipy.ndimage.imread(img_mem, mode='RGB')
        out = enhancer.process(img)
        new_image = create_image_from_array(current_user.id, out, root_id, user_image.id)
    except BaseException as fk:
        app.logger.error(fk)
        abort(500, Response('There was an error check the logs'))

    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())
