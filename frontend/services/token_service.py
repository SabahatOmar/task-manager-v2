from flask import session

def get_headers():
    user_id = session.get('user_id')
    headers = {'Authorization': f"Bearer {session.get('access_token')}"}
    return user_id, headers

def set_session(header):
    #print (header['user_id'])
    #print(header['token'])
    print (header)
    session['user_id'] = header['user_id']
    session['access_token'] = header['token']  # Save the token


def get_userid():
    return session.get('user_id')


def logout_user():
    session.pop('user_id', None)
    session.pop('access_token', None)  # <— also remove the JWT!
