import base64
import tempfile
from io import BytesIO
from rembg.cli import remove
from PIL import Image
from flask import Blueprint, request, abort, Response
from flask_login import login_required, current_user

from app import db
from helpers import return_as_json, return_as_json_list
from image_processing_schemas import extract_faces_schema, remove_background_schema
from orm import UserImage

'''
   This script enhance images with unaligned faces in a folder and paste it back to the original place.
   '''
import dlib
import os
import cv2
import numpy as np
from tqdm import tqdm
from skimage import transform as trans
from skimage import io
from flask_expects_json import expects_json
import torch
from utils import utils
from options.test_options import TestOptions
from models import create_model

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


@image_processing.route('/remove_background', methods=['POST'])
@login_required
@expects_json(remove_background_schema)
def remove_background():
    user_image = UserImage.query.filter_by(id=request.json['image_id'], user_id=current_user.id).first()
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

@image_processing.route('/extract_faces', methods=['POST'])
@login_required
@expects_json(extract_faces_schema)
def extract_faces():
    user_image = UserImage.query.filter_by(id=request.json['image_id'], user_id=current_user.id).first()
    if user_image is None:
        abort(400, Response("No such image"))
    root_id = user_image.root_id
    if user_image.root_id == 0:
        root_id = user_image.id  # make sure we have the right root id

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        encoded_image = user_image.data.encode('utf-8')
        img_bytes = base64.b64decode(encoded_image)
        tmp.write(img_bytes)
    img = dlib.load_rgb_image(tmp.name)
    os.remove(tmp.name)
    aligned_faces, tform_params = detect_and_align_faces(img, face_detector, lmk_predictor, template_path)
    if len(aligned_faces) == 0:
        return return_as_json({'faces': []})

    hq_faces, lq_parse_maps = enhance_faces(aligned_faces, enhance_model)
    hq_images = []

    for hq_face in hq_faces:
        image_data_np = Image.fromarray(hq_face)
        buffered = BytesIO()
        image_data_np.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue())
        new_image = UserImage(parent_id=user_image.id, user_id=current_user.id, data=image_data,
                              root_id=root_id)
        db.session.add(new_image)
        hq_images.append(new_image)
    db.session.commit()
    db.session.flush()
    return return_as_json_list(hq_images)
