
extract_faces_schema = {
    'type': 'object',
    'properties': {
        'image_id': {'type': 'number'},

    },
    'required': ['image_id' ]
}

remove_background_schema = {
    'type': 'object',
    'properties': {
        'image_id': {'type': 'number'},

    },
    'required': ['image_id' ]
}