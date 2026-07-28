from fastapi.testclient import TestClient


def test_list_tasks_is_empty(client: TestClient) -> None:
    """A fresh database should contain no tasks."""

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client: TestClient) -> None:
    """A valid task should be created successfully."""

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Pytest",
            "description": "Write automated API tests",
            "completed": False,
        },
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Learn Pytest"
    assert data["description"] == "Write automated API tests"
    assert data["completed"] is False
    assert data["id"] is not None


def test_get_task_by_id(client: TestClient) -> None:
    """A created task should be retrievable by its ID."""

    create_response = client.post(
        "/tasks",
        json={
            "title": "Read a task",
            "description": "Test the GET endpoint",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Read a task"


def test_update_task(client: TestClient) -> None:
    """PATCH should update only the supplied fields."""

    create_response = client.post(
        "/tasks",
        json={
            "title": "Incomplete task",
            "description": "This task will be updated",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["completed"] is True
    assert data["title"] == "Incomplete task"
    assert data["description"] == "This task will be updated"


def test_delete_task(client: TestClient) -> None:
    """A deleted task should no longer be available."""

    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete this task",
            "description": None,
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": f"Task with id {task_id} was not found."
    }


def test_create_task_with_empty_title(client: TestClient) -> None:
    """An empty title should be rejected by validation."""

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "Invalid task",
            "completed": False,
        },
    )

    assert response.status_code == 422