import base64
from json import dumps

from flask import Response


def return_as_json(data):
    return Response(dumps(data), status=200, mimetype='application/json')


def return_as_json_list(lst):
    return Response(dumps(list(map(lambda x: x.to_dict(), lst))), status=200, mimetype='application/json')

def base64_to_bytes(data):
    return base64.b64decode(data.encode('utf-8'))