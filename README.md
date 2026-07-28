# Developer Workspace Assistant

A Python backend application built with FastAPI for managing developer tasks through a REST API.

The project currently provides complete CRUD operations, input validation, automatic API documentation, error handling, and persistent storage using SQLite.

## Features

- Create developer tasks
- Retrieve all tasks
- Retrieve a task by ID
- Partially update an existing task
- Delete a task
- Validate request data
- Return appropriate HTTP status codes
- Handle missing tasks with `404 Not Found`
- Store data persistently using SQLite
- Generate interactive API documentation automatically

## Technologies

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn
- Git and GitHub
- Pytest
- FastAPI TestClient
- In-memory SQLite testing

## Project Structure

```text
developer-workspace-assistant/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Return basic application information |
| `GET` | `/health` | Check application health |
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | Retrieve all tasks |
| `GET` | `/tasks/{task_id}` | Retrieve one task by ID |
| `PATCH` | `/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/omar-alnadhari/developer-workspace-assistant.git
cd developer-workspace-assistant
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
fastapi dev app/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI generates interactive documentation automatically.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Example: Create a Task

Request:

```http
POST /tasks
Content-Type: application/json
```

Body:

```json
{
  "title": "Learn Docker",
  "description": "Study Docker images and containers",
  "completed": false
}
```

Example response:

```json
{
  "title": "Learn Docker",
  "description": "Study Docker images and containers",
  "completed": false,
  "id": 1
}
```

## Data Persistence

Tasks are stored locally in an SQLite database named:

```text
tasks.db
```

The database file is excluded from Git using `.gitignore` because it contains local runtime data. The application creates the database and its tables automatically when it starts.

## Current Status

The application currently includes:

- FastAPI project structure
- RESTful CRUD endpoints
- Pydantic and SQLModel validation
- SQLite persistence
- Error handling
- Pagination support
- Interactive OpenAPI documentation

## Automated Tests

The project includes automated API tests covering:

- Empty task-list behaviour
- Task creation
- Task retrieval by ID
- Partial task updates
- Task deletion
- `404 Not Found` handling
- Empty-title validation

Run the complete test suite with:

```powershell
python -m pytest -v
```

Expected result:

```text
6 passed
```

The tests use a separate in-memory SQLite database, so they do not modify the local `tasks.db` database.

## Planned Improvements

- Docker containerisation
- Continuous integration using GitHub Actions
- MCP server integration using FastMCP
- Environment-based configuration
- Cloud deployment

## Author

**Omar Al-Nadhari**

- GitHub: [omar-alnadhari](https://github.com/omar-alnadhari)
- LinkedIn: [Omar Al-Nadhari](https://www.linkedin.com/in/omar-al-nadhari)