# E-commerce con Chat IA

## Descripción
API REST de e-commerce de zapatos con chat inteligente usando Clean Architecture.

## Tecnologías
- Python 3.11
- FastAPI
- SQLAlchemy
- Google Gemini AI
- Docker
- Pytest

## Instalación

### Requisitos Previos
- Python 3.10+
- Docker y Docker Compose
- API Key de Google Gemini

### Pasos

1. Clonar repositorio
```bash
git clone https://github.com/josevegara04/TALLER-CONSTRUCCION-2.git
cd taller-construccion-2
```

2. Ejecutar con Docker
```bash
docker-compose up --build
```

## Uso

- API y endpoints: http://localhost:8000

## Endpoints

- GET /products - Lista todos los productos
- GET /products/{id} - Obtiene un producto
- POST /chat - Envía mensaje al chat
- GET /chat/history/{session_id} - Obtiene historial
- GET /health

## Tests

```bash
pytest
```

## Autor
[José Benjamín Vega Ramírez] - Universidad EAFIT