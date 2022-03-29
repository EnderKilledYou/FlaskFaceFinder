image_upload_schema = {
    'type': 'object',
    'properties': {
        'image': {'type': 'string'},
    },
    'required': ['image']
}
get_image_schema = {
    'type': 'object',
    'properties': {
        'image_id': {'type': 'number'},
    },
    'required': ['image_id']
}
