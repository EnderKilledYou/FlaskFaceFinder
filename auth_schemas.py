signup_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password','name']
}

login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}
