# Developer Workspace Assistant

[![Continuous Integration](https://github.com/omar-alnadhari/developer-workspace-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/omar-alnadhari/developer-workspace-assistant/actions/workflows/ci.yml)

A Python backend application built with FastAPI for managing developer tasks through both a REST API and Model Context Protocol (MCP) tools.

The project provides complete CRUD operations, request validation, automatic OpenAPI documentation, SQLite persistence, automated testing, Docker containerisation, continuous integration, and a FastMCP server that allows AI agents to interact with the task-management system.

## Features

- Create, retrieve, update, and delete developer tasks
- Retrieve task collections with pagination
- Validate request data using Pydantic and SQLModel
- Return appropriate HTTP status codes
- Handle missing resources with `404 Not Found`
- Store tasks persistently using SQLite
- Configure the database through environment variables
- Generate Swagger UI and ReDoc documentation automatically
- Run automated REST API and MCP integration tests
- Package and run the application using Docker
- Preserve SQLite data using a named Docker volume
- Run automated tests and Docker builds through GitHub Actions
- Expose task-management operations as MCP tools using FastMCP
- Run the MCP server over Streamable HTTP transport

## Technologies

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn
- Pytest
- FastAPI TestClient
- In-memory SQLite testing
- Model Context Protocol (MCP)
- FastMCP
- Streamable HTTP transport
- Docker
- Docker volumes
- GitHub Actions
- Environment variables
- Git and GitHub

## Project Structure

```text
developer-workspace-assistant/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── mcp_server.py
│   └── models.py
│
├── scripts/
│   └── mcp_http_client.py
│
├── tests/
│   ├── conftest.py
│   ├── test_mcp.py
│   └── test_tasks.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
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
- SQLite persistent storage
- Pagination support
- Environment-based database configuration
- Error handling and appropriate HTTP status codes
- Interactive OpenAPI documentation
- Automated REST API tests
- Automated MCP integration tests
- Docker containerisation
- Persistent Docker volumes
- GitHub Actions continuous integration
- Automated Docker image builds
- FastMCP tool generation from FastAPI operations
- Streamable HTTP MCP server
- Example HTTP MCP client

## Automated Tests

The project includes automated tests covering:

- Empty task-list behaviour
- Task creation
- Task retrieval by ID
- Partial task updates
- Task deletion
- `404 Not Found` handling
- Empty-title validation
- MCP tool discovery
- Exclusion of human-facing endpoints from MCP
- Real MCP execution of `create_task`
- Real MCP execution of `list_tasks`
- Structured MCP response validation

Run the complete test suite with:

```powershell
python -m pytest -v
```

Expected result:

```text
8 passed
```

The tests use a separate in-memory SQLite database, so they do not modify the local `tasks.db` database.

## Continuous Integration

GitHub Actions automatically validates the project on every push and pull request targeting the `main` branch.

The CI workflow performs two jobs:

1. **Run automated tests**
   - Set up Python
   - Install project dependencies
   - Run the complete Pytest suite

2. **Build Docker image**
   - Run only after the tests succeed
   - Set up Docker Buildx
   - Build the application image without publishing it

The workflow ensures that both the Python application and the Docker configuration remain valid after every change.

## MCP Integration

The application exposes its task-management operations as Model Context Protocol tools using FastMCP.

Available MCP tools:

- `create_task`
- `list_tasks`
- `get_task`
- `update_task`
- `delete_task`

The FastAPI root and health-check endpoints are excluded because they are intended for users and monitoring rather than AI-agent actions.

FastMCP generates the MCP tools from the FastAPI OpenAPI schema. Explicit FastAPI `operation_id` values provide short and stable tool names.

The MCP integration tests verify:

- MCP tool discovery
- Exclusion of non-agent endpoints
- Real execution of `create_task`
- Real execution of `list_tasks`
- Structured task responses

## Running the MCP Server over HTTP

Start the MCP server:

```powershell
python -m app.mcp_server
```

The MCP endpoint will be available at:

```text
http://127.0.0.1:8001/mcp
```

The server uses Streamable HTTP transport.

The host and port can be configured using:

```text
MCP_HOST
MCP_PORT
```

Default values:

```text
MCP_HOST=127.0.0.1
MCP_PORT=8001
```

Do not expect the `/mcp` endpoint to display a normal web page. It is a protocol endpoint intended for MCP-compatible clients.

### Example HTTP MCP Client

Leave the MCP server running, open a second terminal, and execute:

```powershell
python scripts/mcp_http_client.py
```

The example client will:

1. Connect to the MCP HTTP endpoint
2. Display the available MCP tools
3. Create a task using `create_task`
4. Retrieve stored tasks using `list_tasks`

The complete request flow is:

```text
MCP Client
    ↓ Streamable HTTP
FastMCP Server
    ↓
FastAPI Operations
    ↓
SQLModel
    ↓
SQLite Database
```
## Environment Configuration

The application supports environment-based configuration.

### Database Configuration

The default local database URL is:

```text
sqlite:///tasks.db
```

A different location can be supplied using:

```text
DATABASE_URL
```

Example Docker value:

```text
DATABASE_URL=sqlite:////data/tasks.db
```

### MCP Server Configuration

The MCP server supports:

```text
MCP_HOST
MCP_PORT
```

Default values:

```text
MCP_HOST=127.0.0.1
MCP_PORT=8001
```

## Docker

Build the Docker image:

```bash
docker build -t developer-workspace-assistant .
```

Create a persistent Docker volume:

```bash
docker volume create developer-workspace-data
```

Run the application with persistent SQLite storage:

```bash
docker run -d --name developer-workspace-api -p 8000:8000 -e DATABASE_URL=sqlite:////data/tasks.db -v developer-workspace-data:/data developer-workspace-assistant
```

View the running container:

```bash
docker ps
```

View application logs:

```bash
docker logs developer-workspace-api
```

Stop and remove the container:

```bash
docker stop developer-workspace-api
docker rm developer-workspace-api
```

The named Docker volume preserves the SQLite database even after the container is removed.

The Docker image is also built automatically by the GitHub Actions CI workflow after all automated tests pass.

## Planned Improvements

- Docker Compose for running the REST API and MCP server together
- Expanded MCP CRUD integration tests
- Cloud deployment

## Author

**Omar Al-Nadhari**

- GitHub: [omar-alnadhari](https://github.com/omar-alnadhari)
- LinkedIn: [Omar Al-Nadhari](https://www.linkedin.com/in/omar-al-nadhari)