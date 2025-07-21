# # PwnageBox

PwnageBox is a project designed to create a secure and efficient environment for testing AI modules and exposing them via a FastAPI backend. The application uses Docker for containerization and SQLite for persistent storage.

## Features

- AI modules for different purposes.
- FastAPI backend for API exposure.
- Dockerfile for containerizing the application.
- SQLite database integration.

## Requirements

- Python 3.8 or newer
- Docker
- Poetry (for dependency management)

## Setup

### Prerequisites
- Python 3.8 or newer
- Poetry
- Docker

### Install dependencies
```bash
poetry install
```

### Run locally
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t pwnagebox .
docker run -d -p 8000:8000 pwnagebox
```

## API Documentation

Access the API documentation at `http://localhost:8000/docs` when the server is running.

## Modules

- AI modules are located in the `ai_modules` directory.
- Each module can be accessed via API endpoints.

## Database

- The application uses SQLite for storage.
- Database file is located at `./data/database.db`.
