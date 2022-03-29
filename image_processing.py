import base64
from flask import Blueprint, request, abort, Response


image_processing = Blueprint('image_processing', __name__)
