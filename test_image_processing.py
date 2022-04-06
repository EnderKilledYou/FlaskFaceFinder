import json

from app import app


def test_remove_background():
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

    response3 = client.get('/extract_faces/' + str(data2['id'])                           )
    data3 = response3.json
    assert len(data3['faces']) == 3
    print(data3['faces'][0]['id'])

    response4 = client.get('/remove_background/'+ str(data3['faces'][0]['id']))

    assert response4.status_code == 200
    data4 = response4.json
    print(data4['id'])

def test_extract_faces():
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

    response3 = client.get('/extract_faces/' + str(data2['id']))
    data3 = response3.json
    assert response3.status_code == 200
    assert len(data3['faces']) == 3

