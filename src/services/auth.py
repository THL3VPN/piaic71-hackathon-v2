from __future__ import annotations

import dataclasses
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import base64
import hashlib
import hmac
import json

logger = logging.getLogger(__name__)

SECRET_ENV = "BETTER_AUTH_SECRET"
ALGORITHM = "HS256"


class AuthError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def get_shared_secret() -> str:
    secret = os.getenv(SECRET_ENV)
    if not secret:
        logger.error("%s is required for JWT auth", SECRET_ENV)
        raise RuntimeError(f"{SECRET_ENV} is required for JWT auth")
    return secret


@dataclass
class AuthenticatedContext:
    user_id: str
    issued_at: datetime | None
    expires_at: datetime | None
    raw_claims: dict[str, Any]


def _auth_error(message: str) -> JSONResponse:
    payload = {"detail": message}
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=payload)


def parse_authorization_header(request: Request) -> str:
    header = request.headers.get("authorization")
    if not header:
        raise AuthError("Authorization header missing")
    parts = header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthError("Authorization header must use Bearer token")
    return parts[1]


def decode_token(token: str) -> dict[str, Any]:
    segments = token.split(".")
    if len(segments) != 3:
        raise AuthError("Malformed token")
    header_b64, payload_b64, signature_b64 = segments
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected = hmac.new(
        get_shared_secret().encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    signature = _b64decode(signature_b64)
    if not hmac.compare_digest(expected, signature):
        raise AuthError("Invalid or expired token")
    payload_json = _b64decode(payload_b64).decode("utf-8")
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as exc:
        logger.debug("JWT payload decode failed: %s", exc)
        raise AuthError("Invalid token payload")
    expires = payload.get("exp")
    if expires and datetime.fromtimestamp(int(expires), timezone.utc) < datetime.now(timezone.utc):
        raise AuthError("Invalid or expired token")
    return payload


def _b64decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def build_authenticated_context(payload: dict[str, Any]) -> AuthenticatedContext:
    sub = payload.get("sub") or payload.get("user_id")
    if not sub:
        raise AuthError("Token missing subject")
    issued_at = _from_timestamp(payload.get("iat"))
    expires_at = _from_timestamp(payload.get("exp"))
    return AuthenticatedContext(
        user_id=str(sub),
        issued_at=issued_at,
        expires_at=expires_at,
        raw_claims=payload,
    )


def _from_timestamp(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (TypeError, ValueError):
        return None


async def require_authorization(request: Request) -> AuthenticatedContext:
    token = getattr(request.state, "raw_token", None)
    if token is None:
        token = parse_authorization_header(request)
    payload = decode_token(token)
    context = build_authenticated_context(payload)
    request.state.auth = context
    return context


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow CORS preflight without auth
        if request.method.upper() == "OPTIONS":
            return await call_next(request)
        try:
            token = parse_authorization_header(request)
            request.state.raw_token = token
        except AuthError as exc:
            payload = {"detail": exc.detail}
            return JSONResponse(status_code=exc.status_code, content=payload)
        response = await call_next(request)
        return response


def get_authenticated_context(request: Request) -> AuthenticatedContext:
    context = getattr(request.state, "auth", None)
    if not isinstance(context, AuthenticatedContext):
        raise AuthError("Authentication context missing")
    return context
