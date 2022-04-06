import base64
import tempfile
from io import BytesIO
from rembg.cli import remove
from PIL import Image
from flask import Blueprint, request, abort, Response
from flask_login import login_required, current_user

from app import db, app
from helpers import return_as_json, return_as_json_list, list_to_dict
from image_processing_schemas import extract_faces_schema, remove_background_schema
from orm import UserImage

from flask_expects_json import expects_json


from test_enhance_single_unalign import *

image_processing = Blueprint('image_processing', __name__)

print("Face Req Loading... ")

face_detector = dlib.cnn_face_detection_model_v1('./pretrain_models/mmod_human_face_detector.dat')
lmk_predictor = dlib.shape_predictor('./pretrain_models/shape_predictor_5_face_landmarks.dat')
template_path = './pretrain_models/FFHQ_template.npy'
face_detector = dlib.get_frontal_face_detector()
opt = TestOptions().parse()
opt.gpus = 0
enhance_model = def_models(opt)
print("Face Req Loaded... ")



@image_processing.route('/remove_background/<image_id>', methods=['GET'])
@login_required
def remove_background(image_id):
    user_image = UserImage.query.filter_by(id=image_id, user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    root_id = user_image.root_id
    if user_image.root_id == 0:
        root_id = user_image.id  # make sure we have the right root id
    img_bytes = base64.b64decode(user_image.data)
    img_bytes_out = remove(img_bytes)
    image_data = base64.b64encode(img_bytes_out)
    new_image = UserImage(parent_id=user_image.id, user_id=current_user.id, data=image_data,
                          root_id=root_id)
    db.session.add(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json(new_image.to_dict())

@image_processing.route('/extract_faces/<image_id>', methods=['GET'])
@login_required
def extract_faces(image_id):
    current_user_id = current_user.id
    user_image = UserImage.query.filter_by(id=image_id, user_id=current_user_id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    root_id = user_image.root_id
    user_image_id = user_image.id
    if user_image.root_id == 0:
        root_id = user_image_id  # make sure we have the right root id

    img = get_image_as_dlib(user_image)

    aligned_faces, tform_params = detect_and_align_faces(img, face_detector, lmk_predictor, template_path)
    if len(aligned_faces) == 0:
        return return_as_json({'faces': list_to_dict([]), 'enhanced': None})

    hq_faces, lq_parse_maps = enhance_faces(aligned_faces, enhance_model)
    hq_images = []
    try:
        for hq_img in hq_faces:
            new_image = create_image_from_array(current_user_id, hq_img, root_id, user_image_id)
            db.session.add(new_image)
            hq_images.append(new_image)
    except BaseException as e:
        app.logger.error(e)
        return Response("Check the logs", status=500)

    try:
        hq_img = past_faces_back(img, hq_faces, tform_params, upscale=opt.test_upscale)
        new_image = create_image_from_array(current_user_id, hq_img, root_id, user_image_id)
        db.session.add(new_image)
    except BaseException as e:
        app.logger.error(e)
        return Response("Check the logs", status=500)

    db.session.commit()
    db.session.flush()

    return return_as_json({'faces': list_to_dict(hq_images), 'enhanced': new_image.to_dict()})


def get_image_as_dlib(user_image):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        encoded_image = user_image.data.encode('utf-8')
        img_bytes = base64.b64decode(encoded_image)
        tmp.write(img_bytes)
    img = dlib.load_rgb_image(tmp.name)
    os.remove(tmp.name)
    return img


def create_image_from_array(current_user_id, hq_img, root_id, user_image_id):
    image_data_np = Image.fromarray(hq_img)
    buffered = BytesIO()
    image_data_np.save(buffered, format="PNG")
    image_data = base64.b64encode(buffered.getvalue())
    new_image = UserImage(parent_id=user_image_id, user_id=current_user_id, data=image_data,
                          root_id=root_id)
    return new_image
