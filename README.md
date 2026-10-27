# DevSecOps Lab — Fase 1

Aplicación Flask mínima para demostrar prácticas de CI/CD y añadir progresivamente SAST, análisis de imágenes Docker, DAST y gestión de hallazgos en DefectDojo.

## Requisitos
- Docker Desktop (motor Docker y Docker Compose)
- Git (para subir a GitHub)
- Python 3.12 opcional para ejecutar pruebas fuera de contenedores

## Ejecutar (PowerShell, dentro de esta carpeta)
```powershell
docker compose up --build -d
docker compose ps
curl.exe http://localhost:8080/health
```
Abrir http://localhost:8080 en el navegador.

## Ejecutar tests sin Docker
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m pytest -q
```

## Detener
```powershell
docker compose down
```

## GitHub Actions
Publicar el contenido de esta carpeta en un repositorio GitHub. El archivo `.github/workflows/ci.yml` ejecuta pruebas y construye la imagen en cada push/pull request.

## Etapas siguientes (aún no implementadas)
- Fase 2: SAST con Semgrep.
- Fase 3: escaneo de imagen con Trivy.
- Fase 4: DAST pasivo con OWASP ZAP sobre un entorno de pruebas autorizado.
- Fase 5: DefectDojo y reglas de aprobación.

No hay resultados de análisis de seguridad hasta que se ejecuten esas etapas. No se han incorporado vulnerabilidades deliberadas.
