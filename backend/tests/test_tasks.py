import json
from http.client import responses


def get_access_token(client):
    client.post('auth/register', json={
        'username': 'testuser2',
        'password': 'testpassword',
        'email': 'testemail'

    })

    response = client.post('auth/login', json={
        'username': 'testuser2',
        'password': 'testpassword'
    })
    data = response.get_json()
    headers = data['token']
    #token = headers['token']

    return headers

def test_create_task(client):
    token = get_access_token(client)
    response = client.post('/tasks/', json={
        'title': 'testtitle',
        'description': 'testdescription',
        'priority': 'low'},
        headers={'Authorization': f'Bearer {token}'}
    )
    print(response.status_code)
    print(response.get_data(as_text=True))

    assert response.status_code ==200
    message = response.get_json()
    assert message['message'] == 'Task created successfully'

def test_get_tasks(client):
    token = get_access_token(client)
    response = client.post('/tasks/', json={
        'title': 'testtitle',
        'description': 'testdescription',
        'priority': 'low'},
        headers={'Authorization': f'Bearer {token}'}
    )
    client.get('/tasks/')
    response = client.get('/tasks/' ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    tasks  = response.get_json()
    assert isinstance(tasks, list)
    assert len(tasks)>0

def test_delete_task(client):
    token = get_access_token(client)
    response = client.post('/tasks/', json={
        'title': 'testtitle',
        'description': 'testdescription',
        'priority': 'low'},
        headers={'Authorization': f'Bearer {token}'}
    )
    response = client.delete('/tasks/1' ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted successfully'

