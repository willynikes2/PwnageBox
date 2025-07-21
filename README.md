```markdown
# PwnageBox

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

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PwnageBox.git
   cd PwnageBox
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

4. Build and run with Docker:
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

```
