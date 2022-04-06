import base64
import os
import subprocess
import tempfile

from flask import Response
from werkzeug.exceptions import abort


def run_python_and_get_image_output(user_image, cmd):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        encoded_image = user_image.data.encode('utf-8')
        img_bytes = base64.b64decode(encoded_image)
        tmp.write(img_bytes)
    sub = subprocess.Popen(cmd(tmp), stdout=subprocess.PIPE, shell=True)
    (output, err) = sub.communicate()
    ## Wait for date to terminate. Get return returncode ##
    p_status = sub.wait()
    if p_status != 0:
        abort(500, Response('There was an error processing your request ' + '(' + p_status + ') ' + output + err))
    with open(tmp.name, "r") as temp_file:
        image_data = base64.b64encode(temp_file.read())
    os.remove(tmp.name)
    return image_data


def image_neural_files(tmp):
    return '/path/to/good/python/for/this/lib /path/to/enhance/script.py --type=photo --model=repair --zoom=1' ' ' + tmp.name


def image_neural_enhance(user_image):
    return run_python_and_get_image_output(user_image, image_neural_files)