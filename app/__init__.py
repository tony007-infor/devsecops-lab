from flask import Flask, jsonify, render_template_string


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    @app.get('/')
    def home():
        return render_template_string('''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>DevSecOps Lab</title><style>body{font-family:system-ui,sans-serif;background:#101827;color:#f3f7ff;margin:0;display:grid;place-items:center;min-height:100vh}main{padding:36px;border:1px solid #37435b;border-radius:18px;max-width:620px;background:#17223a}small{color:#8eb0e0}a{color:#91c7ff}</style></head><body><main><small>LABORATORIO ACADÉMICO</small><h1>DevSecOps Lab</h1><p>Aplicación de prueba para integración CI/CD, SAST, DAST, Trivy y DefectDojo.</p><p>Estado del servicio: <strong>activo</strong></p><a href="/health">Consultar /health</a></main></body></html>''')

    @app.get('/health')
    def health():
        return jsonify(status='ok', service='devsecops-lab'), 200

    @app.after_request
    def add_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    return app
