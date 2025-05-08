def test_register(client):
    response =  client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testemail'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_login(client):
    client.post('/auth/register', json={
        'username': 'testuser2',
        'password': 'testpassword',
        'email': 'testemail'
    })

    response =     client.post('/auth/login', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data