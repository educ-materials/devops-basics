import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.database import init_database
from app.main import app, get_db


@pytest.fixture
def test_database(tmp_path):

    database_path = tmp_path / "test.db"

    init_database(database_path)

    return database_path


@pytest.fixture
def client(test_database):

    def get_test_db():

        connection = sqlite3.connect(test_database)

        connection.row_factory = sqlite3.Row

        try:
            yield connection
        finally:
            connection.close()

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_tasks(client):

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):

    response = client.post(
        "/api/tasks",
        json={
            "title": "Learn CI/CD"
        },
    )

    assert response.status_code == 201

    task = response.json()

    assert task["title"] == "Learn CI/CD"
    assert task["completed"] == 0
    assert "id" in task


def test_update_task(client):

    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Original task"
        },
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated task",
            "completed": True,
        },
    )

    assert response.status_code == 200

    task = response.json()

    assert task["id"] == task_id
    assert task["title"] == "Updated task"
    assert task["completed"] == 1


def test_delete_task(client):

    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Task to delete"
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204

    response = client.get("/api/tasks")

    tasks = response.json()

    assert not any(task["id"] == task_id for task in tasks)


def test_delete_nonexistent_task(client):

    response = client.delete("/api/tasks/999999")

    assert response.status_code == 404