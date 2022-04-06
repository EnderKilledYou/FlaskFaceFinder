import base64
import os
import subprocess
import tempfile

from flask import Response
from werkzeug.exceptions import abort

from orm import UserImage


def run_python_and_get_image_output(cmd):
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = sub.communicate()
    ## Wait for date to terminate. Get return returncode ##
    p_status = sub.wait()
    if p_status != 0:
        abort(500, Response('There was an error processing your request ' + '(' + p_status + ') ' + output + err))


def image_neural_files(file):
    return '/path/to/good/python/for/this/lib /path/to/enhance/script.py --type=photo --model=repair --zoom=1' + file


def image_neural_enhance(user_image):
    file = user_image.write_to_file()
    run_python_and_get_image_output(image_neural_files(file))
    return UserImage.read_from_file(file, user_image)
