import base64
import io
import json
import tempfile
from dataclasses import dataclass

from flask_sqlalchemy import Model

from app import db
from flask_login import UserMixin
from flask import Blueprint
from sqlalchemy_serializer import SerializerMixin

orm = Blueprint('orm', __name__)


class User(UserMixin, db.Model, SerializerMixin):
    serialize_rules = ()
    serialize_only = ('id', 'email', 'name')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class UserImage(db.Model, SerializerMixin):
    serialize_only = ('id', 'parent_id', 'root_id', 'user_id', 'data')
    serialize_rules = ()
    id = db.Column(db.Integer, primary_key=True, index=True)
    root_id = db.Column(db.Integer, index=True)
    parent_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    data = db.Column(db.Text)

    def to_bytesio(self):
        img_bytes = base64.b64decode(self.data)
        img_mem = io.BytesIO()
        img_mem.write(img_bytes)
        img_mem.seek(0)
        return img_mem

    def write_to_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            encoded_image = self.data.encode('utf-8')
            img_bytes = base64.b64decode(encoded_image)
            tmp.write(img_bytes)
        return tmp.name

    def read_from_PIL(self, out):
        root_id = self.root_id
        if self.root_id == 0:
            root_id = self.id
        buffered = io.BytesIO()
        out.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue())
        return UserImage(parent_id=self.parent_id, user_id=self.user_id, data=image_data,
                         root_id=root_id)

    @staticmethod
    def read_from_file(file_path, parent_image=None):
        with open(file_path, "r") as temp_file:
            image_data = base64.b64encode(temp_file.read())
        if parent_image is None:
            return UserImage(data=image_data)
        root_id = parent_image.root_id
        if parent_image.root_id == 0:
            root_id = parent_image.id
        return UserImage(parent_id=parent_image.parent_id, user_id=parent_image.user_id, data=image_data,
                         root_id=root_id)
