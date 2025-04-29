def test_register(client):
    response =  client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })

    response =     client.post('/api/auth/login', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data