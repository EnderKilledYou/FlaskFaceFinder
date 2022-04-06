import json

from app import app


def test_enhances():
    client = app.test_client()
    with open("testimage.base64", "r") as data_file:
        base64_content = data_file.read()
        upload_data = json.dumps({'image': base64_content})

    response = client.post('/login',
                           data=json.dumps({'email': 'someg8ggbggg6g85gv4g77@place.com',
                                            'password': 'abcd123applebanana'}),
                           content_type='application/json', )
    data = response.json

    assert response.status_code == 200

    response2 = client.get('/neural_enhance/' + data['id'])
    assert response2.status_code == 200
    data2 = response2.json


