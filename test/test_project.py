import pytest


def test_home_route(client):
    response = client.get('/api/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Welcome to the Home Route!'


def test_blog_route(client):
    response = client.get('/api/blog/')
    # print(response.status_code)
    # assert response.status_code == 200
    data = response.get_json()
    # assert data['message'] == 'Welcome to the Home Route!'

def test_get_all_metadata(app):
    from app.services.metadata_db_services import create_metadata_entry, get_all_metadata_entry
    with app.app_context():
        create_metadata_entry('Blog App','My Awesome Blog App','/blog/app','github.com/path')
        list = get_all_metadata_entry()
        print('list:', list)
        
    