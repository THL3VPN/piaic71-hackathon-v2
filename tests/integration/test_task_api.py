from fastapi.testclient import TestClient

from src.main import app

MISSING_TASK_DETAIL = {"detail": "Task not found"}


def test_post_then_get_tasks():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "New Task", "description": "desc"})
        assert post_resp.status_code == 201
        created = post_resp.json()
        assert created["title"] == "New Task"
        assert created["completed"] is False

        get_resp = client.get("/api/tasks")
        assert get_resp.status_code == 200
        tasks = get_resp.json()
        assert any(task["id"] == created["id"] for task in tasks)


def test_get_and_put_task_not_found():
    with TestClient(app) as client:
        get_resp = client.get("/api/tasks/9999")
        assert get_resp.status_code == 404
        assert get_resp.json() == MISSING_TASK_DETAIL

        put_resp = client.put("/api/tasks/9999", json={"title": "Updated", "description": "desc"})
        assert put_resp.status_code == 404
        assert put_resp.json() == MISSING_TASK_DETAIL


def test_update_task_success():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Original", "description": "desc"})
        assert post_resp.status_code == 201
        created = post_resp.json()

        put_resp = client.put(
            f"/api/tasks/{created['id']}",
            json={"title": "Updated Task", "description": "new desc"},
        )
        assert put_resp.status_code == 200
        updated = put_resp.json()
        assert updated["title"] == "Updated Task"
        assert updated["description"] == "new desc"


def test_delete_task_not_found():
    with TestClient(app) as client:
        resp = client.delete("/api/tasks/9999")
        assert resp.status_code == 404
        assert resp.json() == MISSING_TASK_DETAIL


def test_delete_task_success():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "To delete", "description": "desc"})
        assert post_resp.status_code == 201
        created = post_resp.json()

        delete_resp = client.delete(f"/api/tasks/{created['id']}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/tasks/{created['id']}")
        assert get_resp.status_code == 404


def test_toggle_completion():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Toggle", "description": "desc"})
        assert post_resp.status_code == 201
        created = post_resp.json()

        patch_resp = client.patch(f"/api/tasks/{created['id']}/complete")
        assert patch_resp.status_code == 200
        toggled = patch_resp.json()
        assert toggled["completed"] is True

        patch_resp2 = client.patch(f"/api/tasks/{created['id']}/complete")
        assert patch_resp2.status_code == 200
        toggled2 = patch_resp2.json()
        assert toggled2["completed"] is False


def test_create_task_validation_error():
    with TestClient(app) as client:
        resp = client.post("/api/tasks", json={"description": "missing title"})
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert isinstance(detail, list)
        first_error = detail[0]
        assert first_error["loc"][-1] == "title"
        assert first_error["type"] in {"missing", "value_error", "value_error.missing"}


def test_update_task_validation_error():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Original", "description": "desc"})
        assert post_resp.status_code == 201
        created = post_resp.json()

        bad_put = client.put(f"/api/tasks/{created['id']}", json={"title": "", "description": "desc"})
        assert bad_put.status_code == 422
        detail = bad_put.json()["detail"]
        assert detail[0]["loc"][-1] == "title"
