from flask import Flask, jsonify, render_template_string


HOME_HTML = '''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DevSecOps Lab</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <main>
    <small>LABORATORIO ACADÉMICO</small>
    <h1>DevSecOps Lab</h1>
    <p>Aplicación de prueba para integración CI/CD, SAST, DAST, Trivy y DefectDojo.</p>
    <p>Estado del servicio: <strong>activo</strong></p>
    <a href="/health">Consultar /health</a>
  </main>
</body>
</html>'''


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    @app.get('/')
    def home():
        return render_template_string(HOME_HTML)

    @app.get('/health')
    def health():
        return jsonify(status='ok', service='devsecops-lab'), 200

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = (
            "default-src 'none'; "
            "style-src 'self'; "
            "connect-src 'self'; "
            "base-uri 'none'; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers['Permissions-Policy'] = (
            'camera=(), microphone=(), geolocation=()'
        )
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response.headers['Cache-Control'] = 'no-store, max-age=0'
        return response

    return app
