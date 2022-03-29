import json

from app import app


def test_image_upload():
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

    response2 = client.post('/upload_image',
                            data=upload_data,
                            content_type='application/json', )
    data2 = response2.json

    assert response2.status_code == 200


def test_image_get():
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

    response2 = client.post('/upload_image',
                            data=upload_data,
                            content_type='application/json', )
    data2 = response2.json

    image_query = json.dumps({'image_id': data2['id']})
    response3 = client.post('/get_image',
                            data=image_query,
                            content_type='application/json')
    data3 = response3.json

    assert data3['data'] == base64_content


def test_get_images():
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

    response2 = client.post('/upload_image',
                            data=upload_data,
                            content_type='application/json', )
    data2 = response2.json

    assert response2.status_code == 200

    response3 = client.get('/get_images')

    data3 = response3.json

    found = list(filter(
        lambda x: x['id'] == data2['id'],
        data3
    ))
    assert len(found) > 0
