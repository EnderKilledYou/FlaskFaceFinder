import json

from app import app


def test_signup():
    response = app.test_client().post('/signup',
                                      data=json.dumps({'email': 'someg8ggbggg6g85gv4g77@place.com',
                                                       'password': 'abcd123applebanana',
                                                       'name': 'test user'}),
                                      content_type='application/json', )
    data = response.json

    assert response.status_code == 200


def test_login():
    response = app.test_client().post('/login',
                                      data=json.dumps({'email': 'someg8ggbggg6g85gv4g77@place.com',
                                                       'password': 'abcd123applebanana'}),
                                      content_type='application/json', )
    data = response.json

    assert response.status_code == 200

    response = app.test_client().post('/login',
                                      data=json.dumps({'email': 'someg8ggbggg6g85gv4g77@place.com',
                                                       'password': 'wrongpassword'}),
                                      content_type='application/json', )
    data = response.json

    assert response.status_code == 401
