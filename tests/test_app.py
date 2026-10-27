from app import create_app


def test_health():
    client = create_app().test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


def test_home_and_security_headers():
    client = create_app().test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'DevSecOps Lab' in response.data
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'
