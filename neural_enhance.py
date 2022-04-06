import base64
import io
import imageio
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
@neural_enhance.route('/neural_enhance/<id>', methods=['GET'])
@login_required
def neural_enhancer(id):
    user_image: UserImage = UserImage.query.filter_by(id=id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    try:

        img_mem = user_image.to_bytesio()
        img = imageio.imread(img_mem)
        out = enhancer.process(img)
        new_image = user_image.read_from_PIL(out)

    except BaseException as fk:
        app.logger.error(fk)
        abort(500, Response('There was an error check the logs'))

    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())
