from app import create_app


def test_security_headers_on_pages_and_health():
    client = create_app().test_client()
    for path in ('/', '/health', '/static/style.css'):
        response = client.get(path)
        assert response.status_code == 200
        assert "default-src 'none'" in response.headers['Content-Security-Policy']
        assert "style-src 'self'" in response.headers['Content-Security-Policy']
        assert 'unsafe-inline' not in response.headers['Content-Security-Policy']
        assert response.headers['Permissions-Policy'] == 'camera=(), microphone=(), geolocation=()'
        assert response.headers['Cross-Origin-Embedder-Policy'] == 'require-corp'
        assert response.headers['Cache-Control'] == 'no-store, max-age=0'


def test_home_uses_external_css():
    response = create_app().test_client().get('/')
    assert b'/static/style.css' in response.data
    assert b'<style>' not in response.data
