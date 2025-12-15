import os

import jwt
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from src.services.auth import AuthenticatedContext, AuthMiddleware, require_authorization

SECRET = "test-secret"

app = FastAPI()
app.add_middleware(AuthMiddleware)

@app.get("/protected")
async def protected(auth: AuthenticatedContext = Depends(require_authorization)) -> dict[str, str]:
    return {"user_id": auth.user_id}

client = TestClient(app)


@pytest.fixture(autouse=True)
def shared_secret(monkeypatch):
    monkeypatch.setenv("BETTER_AUTH_SECRET", SECRET)


def create_token(sub: str, secret: str = SECRET) -> str:
    return jwt.encode({"sub": sub, "exp": 9999999999}, secret, algorithm="HS256")


def test_missing_authorization_header():
    response = client.get("/protected")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_invalid_auth_header():
    response = client.get("/protected", headers={"Authorization": "Token mismatched"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_invalid_jwt_token():
    token = create_token("123", secret="wrong-secret")
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_valid_jwt_token():
    token = create_token("user-42")
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"user_id": "user-42"}
