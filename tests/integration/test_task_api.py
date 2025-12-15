import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

from fastapi.testclient import TestClient

os.environ.setdefault("BETTER_AUTH_SECRET", "replace-with-shared-secret")
SECRET = os.getenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")

from src.main import app

def _build_token(user_id: str) -> str:
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').rstrip(b"=")
    payload = base64.urlsafe_b64encode(
        json.dumps({"sub": user_id, "exp": int(datetime(2030, 1, 1, tzinfo=timezone.utc).timestamp())}).encode()
    ).rstrip(b"=")
    signing_input = header + b"." + payload
    signature = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=")
    return f"{signing_input.decode()}.{signature_b64.decode()}"

MISSING_TASK_DETAIL = {"detail": "Task not found"}
AUTH_HEADERS = {"Authorization": f"Bearer {_build_token('integration-user')}"}
AUTH_HEADERS_OTHER = {"Authorization": f"Bearer {_build_token('other-user')}"}


def test_post_then_get_tasks():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "New Task", "description": "desc"}, headers=AUTH_HEADERS)
        assert post_resp.status_code == 201
        created = post_resp.json()
        assert created["title"] == "New Task"
        assert created["completed"] is False

        get_resp = client.get("/api/tasks", headers=AUTH_HEADERS)
        assert get_resp.status_code == 200
        tasks = get_resp.json()
        assert any(task["id"] == created["id"] for task in tasks)


def test_get_and_put_task_not_found():
    with TestClient(app) as client:
        get_resp = client.get("/api/tasks/9999", headers=AUTH_HEADERS)
        assert get_resp.status_code == 404
        assert get_resp.json() == MISSING_TASK_DETAIL

        put_resp = client.put("/api/tasks/9999", json={"title": "Updated", "description": "desc"}, headers=AUTH_HEADERS)
        assert put_resp.status_code == 404
        assert put_resp.json() == MISSING_TASK_DETAIL


def test_update_task_success():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Original", "description": "desc"}, headers=AUTH_HEADERS)
        assert post_resp.status_code == 201
        created = post_resp.json()

        put_resp = client.put(
            f"/api/tasks/{created['id']}",
            json={"title": "Updated Task", "description": "new desc"},
            headers=AUTH_HEADERS,
        )
        assert put_resp.status_code == 200
        updated = put_resp.json()
        assert updated["title"] == "Updated Task"
        assert updated["description"] == "new desc"


def test_delete_task_not_found():
    with TestClient(app) as client:
        resp = client.delete("/api/tasks/9999", headers=AUTH_HEADERS)
        assert resp.status_code == 404
        assert resp.json() == MISSING_TASK_DETAIL


def test_delete_task_success():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "To delete", "description": "desc"}, headers=AUTH_HEADERS)
        assert post_resp.status_code == 201
        created = post_resp.json()

        delete_resp = client.delete(f"/api/tasks/{created['id']}", headers=AUTH_HEADERS)
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/tasks/{created['id']}", headers=AUTH_HEADERS)
        assert get_resp.status_code == 404


def test_toggle_completion():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Toggle", "description": "desc"}, headers=AUTH_HEADERS)
        assert post_resp.status_code == 201
        created = post_resp.json()

        patch_resp = client.patch(f"/api/tasks/{created['id']}/complete", headers=AUTH_HEADERS)
        assert patch_resp.status_code == 200
        toggled = patch_resp.json()
        assert toggled["completed"] is True

        patch_resp2 = client.patch(f"/api/tasks/{created['id']}/complete", headers=AUTH_HEADERS)
        assert patch_resp2.status_code == 200
        toggled2 = patch_resp2.json()
        assert toggled2["completed"] is False


def test_create_task_validation_error():
    with TestClient(app) as client:
        resp = client.post("/api/tasks", json={"description": "missing title"}, headers=AUTH_HEADERS)
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert isinstance(detail, list)
        first_error = detail[0]
        assert first_error["loc"][-1] == "title"
        assert first_error["type"] in {"missing", "value_error", "value_error.missing"}


def test_update_task_validation_error():
    with TestClient(app) as client:
        post_resp = client.post("/api/tasks", json={"title": "Original", "description": "desc"}, headers=AUTH_HEADERS)
        assert post_resp.status_code == 201
        created = post_resp.json()

        bad_put = client.put(
            f"/api/tasks/{created['id']}",
            json={"title": "", "description": "desc"},
            headers=AUTH_HEADERS,
        )
        assert bad_put.status_code == 422
        detail = bad_put.json()["detail"]
        assert detail[0]["loc"][-1] == "title"


def test_missing_token_rejected():
    with TestClient(app) as client:
        resp = client.get("/api/tasks")
        assert resp.status_code == 401
        assert "detail" in resp.json()


def test_owned_tasks_only_listed_per_user():
    with TestClient(app) as client:
        # Clean any existing tasks for these users to isolate the test
        for header in (AUTH_HEADERS, AUTH_HEADERS_OTHER):
            resp = client.get("/api/tasks", headers=header)
            if resp.status_code == 200:
                for task in resp.json():
                    client.delete(f"/api/tasks/{task['id']}", headers=header)
        # user A creates two tasks
        for title in ["A1", "A2"]:
            assert client.post("/api/tasks", json={"title": title}, headers=AUTH_HEADERS).status_code == 201
        # user B creates one task
        assert client.post("/api/tasks", json={"title": "B1"}, headers=AUTH_HEADERS_OTHER).status_code == 201

        list_a = client.get("/api/tasks", headers=AUTH_HEADERS)
        assert list_a.status_code == 200
        tasks_a = [t["title"] for t in list_a.json()]
        assert tasks_a == ["A1", "A2"]

        list_b = client.get("/api/tasks", headers=AUTH_HEADERS_OTHER)
        assert list_b.status_code == 200
        tasks_b = [t["title"] for t in list_b.json()]
        assert tasks_b == ["B1"]


def test_cross_user_access_forbidden_or_not_found():
    with TestClient(app) as client:
        create = client.post("/api/tasks", json={"title": "Private"}, headers=AUTH_HEADERS)
        assert create.status_code == 201
        task_id = create.json()["id"]

        # other user should not see/update/delete
        get_other = client.get(f"/api/tasks/{task_id}", headers=AUTH_HEADERS_OTHER)
        assert get_other.status_code in (403, 404)

        put_other = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked", "description": "bad"},
            headers=AUTH_HEADERS_OTHER,
        )
        assert put_other.status_code in (403, 404)

        delete_other = client.delete(f"/api/tasks/{task_id}", headers=AUTH_HEADERS_OTHER)
        assert delete_other.status_code in (403, 404)

        # owner still can delete
        delete_owner = client.delete(f"/api/tasks/{task_id}", headers=AUTH_HEADERS)
        assert delete_owner.status_code == 204
